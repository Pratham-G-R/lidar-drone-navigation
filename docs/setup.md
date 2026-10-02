# Setup and operation

These instructions assemble a bench reconstruction on a ROS 2 Jazzy machine. ROS integration and aircraft validation remain pending. Use the project's existing ROS installation if available and record its versions before changing packages.

## 1. Dependencies and workspace

The intended platform is Ubuntu 24.04 with ROS 2 Jazzy. Confirm the actual Pi installation; the notes establish Jazzy, but not the Ubuntu release. Install ROS following its official instructions first.

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-rosdep python3-yaml \
  ros-jazzy-mavros ros-jazzy-mavros-extras ros-jazzy-slam-toolbox \
  ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-rmw-fastrtps-cpp \
  ros-jazzy-foxglove-bridge
```

MAVROS may also require GeographicLib datasets. Follow the installed MAVROS package's official dataset installation instructions if startup reports missing datasets. Install the RPLidar ROS 2 driver matching your original setup; record its upstream URL, branch and commit. Do not mix launch files from `rplidar_ros` and `sllidar_ros2`.

Place this repository at `~/lidar_ws/src/lidar-drone-navigation`. Then:

```bash
cd ~/lidar_ws
# Initialize rosdep once if it has not already been initialized:
# sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select lidar_drone
source install/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```

Source ROS and the workspace in every terminal. The package maintainer is Pratham; project licensing remains pending.

## 2. Device identity and permissions

```bash
ls -l /dev/serial/by-id/
ls -l /dev/ttyS0 /dev/ttyUSB0
sudo usermod -aG dialout "$USER"
```

Log out and back in after a group change. Prefer stable `/dev/serial/by-id/` paths for USB devices. Confirm that the Pi UART is enabled, not used by a console, and corresponds to the connected pins. The source notes use `/dev/ttyS0` at 921600 baud, but this does not identify the FCU port or prove a working physical connection.

## 3. MAVROS and odometry

With the vehicle disarmed and propellers removed for bench work:

```bash
ros2 run mavros mavros_node --ros-args -r __ns:=/mavros \
  -p fcu_url:=/dev/ttyS0:921600 \
  -p local_position.tf.send:=false \
  -p local_position.frame_id:=odom \
  -p local_position.tf.child_frame_id:=base_link
```

This uses the source connection settings with TF disabled. MAVROS plugin namespace/parameter behavior is version-dependent; inspect the actual nodes and parameters. The archived `gcs_url` value is not reused without a known network endpoint.

```bash
ros2 node list
ros2 topic echo /mavros/state --once
ros2 topic echo /mavros/local_position/odom --once
ros2 topic hz /mavros/local_position/odom
```

Confirm `header.frame_id: odom`, `child_frame_id: base_link`, correct timestamps and a continuous pose estimate. Configure the actual FCU telemetry port to provide the required messages. The manuscript's `SR2_POSITION=10` is a reported setting, not a universal setting for every UART; establish the port mapping first.

## 4. LiDAR and measured transform

Inspect installed launch files before choosing the driver command:

```bash
ros2 pkg prefix --share rplidar_ros
ros2 launch rplidar_ros rplidar.launch.py --show-args
```

`rplidar.launch.py` is the filename in the source notes. If absent, use the matching A1 launch file in the installed driver. Specify the verified serial path/baud using that file's declared arguments. Then inspect `/scan` and its frame ID:

```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
```

Measure the LiDAR pose relative to the selected `base_link` origin. Translation is in metres and rotation in radians. Set `LIDAR_X`, `LIDAR_Y`, `LIDAR_Z`, `LIDAR_YAW`, `LIDAR_PITCH` and `LIDAR_ROLL` to those measured values in your terminal; the command fails if they are missing:

```bash
ros2 run tf2_ros static_transform_publisher \
  --x "${LIDAR_X:?Set measured x offset}" --y "${LIDAR_Y:?Set measured y offset}" \
  --z "${LIDAR_Z:?Set measured z offset}" --yaw "${LIDAR_YAW:?Set measured yaw}" \
  --pitch "${LIDAR_PITCH:?Set measured pitch}" --roll "${LIDAR_ROLL:?Set measured roll}" \
  --frame-id base_link --child-frame-id laser
```

Use the actual scan frame if it is not `laser`, updating the support configuration as well.

## 5. Support nodes and configuration generation

```bash
ros2 launch lidar_drone support.launch.py
```

From the repository root, set `ROBOT_RADIUS` to the measured radius enclosing the vehicle including propellers, then generate templates:

```bash
python3 tools/prepare_configs.py --robot-radius "${ROBOT_RADIUS:?Set measured radius in metres}"
```

The generator preserves installed plugin defaults and writes source hashes. Review the generated Nav2 controller, velocity smoother, inflation, obstacle heights and range limits. Ground-robot controller defaults are not UAV tuning. Generated files are ignored by Git until intentionally reviewed and versioned.

## 6. SLAM and Nav2

In separate terminals from the repository root:

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:="$PWD/config/generated/mapper_params_online_async_gps.yaml" \
  use_sim_time:=false
```

```bash
ros2 launch nav2_bringup navigation_launch.py \
  params_file:="$PWD/config/generated/nav2_params_gps.yaml" \
  use_sim_time:=false autostart:=true use_composition:=false
```

These commands use live SLAM, so do not start AMCL or a competing map-to-odom publisher. Confirm the complete TF chain and that Nav2's final `/cmd_vel` is `geometry_msgs/msg/Twist`. The generator requests unstamped commands; differing installed components must be checked with `ros2 topic info /cmd_vel -v`.

## 7. Visualization and goals

```bash
ros2 run foxglove_bridge foxglove_bridge
ros2 run tf2_ros tf2_echo map laser
ros2 action list -t
```

Connect Foxglove to the Pi's configured bridge endpoint on a trusted network. Add `/scan`, `/map`, `/plan` and the costmap topics, using `map` as the fixed frame. Send a finite `PoseStamped` goal in `map` on `/move_base_simple/goal`, or use a Nav2 action client directly. For a yaw-only quaternion, use `z = sin(yaw/2)` and `w = cos(yaw/2)`.

Monitor `/lidar_drone/gate_status` and `/lidar_drone/cmd_vel_checked`. The vehicle will not execute these commands because no autopilot adapter is included. A stationary bench robot may time out Nav2 progress checking after a goal; that is not proof of a planner failure.

## 8. Record and export

```bash
bash tools/record_bag.sh data/raw/session_001
ros2 run nav2_map_server map_saver_cli -f data/maps/session_001
```

Use a fresh session identifier each time, and save the session metadata described in [data.md](data.md). A map image plus YAML is distinct from a serialized SLAM pose graph; keep both if continuing a mapping session is required.
