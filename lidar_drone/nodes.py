"""New implementations based on the manuscript, not the original flight code.

No node arms, changes mode, takes off, or publishes MAVROS setpoints.
"""
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import qos_profile_sensor_data
from rclpy.clock import Clock, ClockType
from geometry_msgs.msg import PoseStamped, TransformStamped, Twist
from nav_msgs.msg import Odometry
from nav2_msgs.action import NavigateToPose
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, String
from tf2_ros import TransformBroadcaster

from .core import CommandGate, scan_blocked


def positive(node, name, default):
    value = float(node.declare_parameter(name, default).value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be positive and finite')
    return value


class OdomToTF(Node):
    def __init__(self):
        super().__init__('odom_to_tf')
        self.parent = self.declare_parameter('parent_frame', 'odom').value
        self.child = self.declare_parameter('child_frame', 'base_link').value
        self.broadcaster = TransformBroadcaster(self)
        self.create_subscription(Odometry, '/mavros/local_position/odom', self.receive,
                                 qos_profile_sensor_data)
        self.warned = False

    def receive(self, msg):
        if msg.header.frame_id != self.parent or msg.child_frame_id != self.child:
            if not self.warned:
                self.get_logger().error('Odometry frames mismatch; refusing to relabel coordinates.')
                self.warned = True
            return
        p, q = msg.pose.pose.position, msg.pose.pose.orientation
        if not all(math.isfinite(v) for v in (p.x, p.y, p.z, q.x, q.y, q.z, q.w)):
            return
        norm = math.sqrt(q.x*q.x + q.y*q.y + q.z*q.z + q.w*q.w)
        if norm < 1e-6 or abs(norm - 1.0) > 0.05:
            return
        t = TransformStamped()
        t.header = msg.header  # Preserve the incoming timestamp.
        t.child_frame_id = msg.child_frame_id
        t.transform.translation.x, t.transform.translation.y, t.transform.translation.z = p.x, p.y, p.z
        t.transform.rotation.x, t.transform.rotation.y = q.x / norm, q.y / norm
        t.transform.rotation.z, t.transform.rotation.w = q.z / norm, q.w / norm
        self.broadcaster.sendTransform(t)


class GoalRelay(Node):
    """Explicit action client; only one active goal, no implicit preemption."""
    def __init__(self):
        super().__init__('goal_relay')
        self.client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.busy = False
        self.create_subscription(PoseStamped, '/move_base_simple/goal', self.receive, 10)

    def receive(self, msg):
        p, q = msg.pose.position, msg.pose.orientation
        values = (p.x, p.y, p.z, q.x, q.y, q.z, q.w)
        if msg.header.frame_id != 'map' or not all(math.isfinite(v) for v in values):
            self.get_logger().error('Goal requires map frame and finite pose values.')
            return
        if abs(q.x*q.x + q.y*q.y + q.z*q.z + q.w*q.w - 1.0) > 0.01:
            self.get_logger().error('Goal orientation must be a unit quaternion.')
            return
        if self.busy or not self.client.server_is_ready():
            self.get_logger().warning('Goal rejected: action server unavailable or goal already active.')
            return
        goal = NavigateToPose.Goal()
        goal.pose = msg
        self.busy = True
        self.client.send_goal_async(goal).add_done_callback(self.accepted)

    def accepted(self, future):
        try:
            handle = future.result()
            if not handle.accepted:
                self.busy = False
                self.get_logger().warning('Nav2 rejected goal.')
                return
            handle.get_result_async().add_done_callback(self.completed)
        except Exception as exc:
            self.busy = False
            self.get_logger().error(str(exc))

    def completed(self, future):
        self.busy = False
        try:
            self.get_logger().info(f'Navigation action ended with status {future.result().status}')
        except Exception as exc:
            self.get_logger().error(str(exc))


class LaserSafetyStop(Node):
    def __init__(self):
        super().__init__('laser_safety_stop')
        self.distance = positive(self, 'stop_distance', 1.0)
        self.timeout = positive(self, 'scan_timeout', 0.5)
        self.fraction = positive(self, 'min_valid_fraction', 0.5)
        if self.fraction > 1:
            raise ValueError('min_valid_fraction must be <= 1')
        self.frame = self.declare_parameter('scan_frame', 'laser').value
        self.last_scan = None
        self.blocked = True
        self.pub = self.create_publisher(Bool, '/lidar_drone/stop', 10)
        self.create_subscription(LaserScan, '/scan', self.receive, qos_profile_sensor_data)
        self.steady = Clock(clock_type=ClockType.STEADY_TIME)
        self.create_timer(0.05, self.tick, clock=self.steady)

    def receive(self, msg):
        self.last_scan = time.monotonic()
        # Receipt-time watchdog. Does not detect old scans replayed at a live rate.
        self.blocked = msg.header.frame_id != self.frame or scan_blocked(
            msg.ranges, msg.range_min, msg.range_max, self.distance, self.fraction)

    def tick(self):
        stale = self.last_scan is None or time.monotonic() - self.last_scan > self.timeout
        self.pub.publish(Bool(data=bool(stale or self.blocked)))


class CmdVelMux(Node):
    def __init__(self):
        super().__init__('cmd_vel_mux')
        self.gate = CommandGate(
            command_timeout=positive(self, 'command_timeout', 0.5),
            safety_timeout=positive(self, 'safety_timeout', 0.3),
            max_speed=positive(self, 'max_speed', 0.3),
            max_yaw_rate=positive(self, 'max_yaw_rate', 0.3))
        self.pub = self.create_publisher(Twist, '/lidar_drone/cmd_vel_checked', 10)
        self.status = self.create_publisher(String, '/lidar_drone/gate_status', 10)
        self.create_subscription(Twist, '/cmd_vel', self.receive, 10)
        self.create_subscription(Bool, '/lidar_drone/stop',
                                 lambda m: self.gate.receive_safety(m.data, time.monotonic()), 10)
        self.steady = Clock(clock_type=ClockType.STEADY_TIME)
        self.create_timer(0.05, self.tick, clock=self.steady)

    def receive(self, msg):
        self.gate.receive_command((msg.linear.x, msg.linear.y, msg.linear.z,
                                   msg.angular.x, msg.angular.y, msg.angular.z), time.monotonic())

    def tick(self):
        (x, y, yaw), reason = self.gate.output(time.monotonic())
        msg = Twist()
        msg.linear.x, msg.linear.y, msg.angular.z = x, y, yaw
        self.pub.publish(msg)
        self.status.publish(String(data=reason))


def run(node_class):
    rclpy.init()
    node = None
    try:
        node = node_class()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


def odom_to_tf(): run(OdomToTF)
def goal_relay(): run(GoalRelay)
def laser_safety_stop(): run(LaserSafetyStop)
def cmd_vel_mux(): run(CmdVelMux)
