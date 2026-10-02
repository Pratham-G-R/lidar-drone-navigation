# Topics, transforms and code behavior

## Transform ownership

| Edge | Sole publisher | Required check |
| --- | --- | --- |
| `map → odom` | SLAM Toolbox | No simultaneous AMCL or second SLAM owner |
| `odom → base_link` | Reconstructed `odom_to_tf` | Disable MAVROS publication of this edge |
| `base_link → laser` | Static transform publisher | Measure translation and rotation; confirm sensor frame name |

`odom_to_tf` checks both incoming frame IDs, finite coordinates and quaternion norm. It normalizes a near-unit quaternion and keeps the incoming timestamp. A different frame ID is rejected, not silently relabeled. No transform is extrapolated after odometry stops. This node does not perform GPS conversion, filtering, time synchronization or localization.

## Topic contract

| Topic | Type | Producer → consumer |
| --- | --- | --- |
| `/scan` | `sensor_msgs/msg/LaserScan` | Driver → SLAM, costmaps, scan watchdog |
| `/mavros/local_position/odom` | `nav_msgs/msg/Odometry` | MAVROS → broadcaster and Nav2 |
| `/tf`, `/tf_static` | `tf2_msgs/msg/TFMessage` | Frame publishers → ROS consumers |
| `/map` | `nav_msgs/msg/OccupancyGrid` | SLAM → global costmap and visualization |
| `/move_base_simple/goal` | `geometry_msgs/msg/PoseStamped` | UI → reconstructed goal relay |
| `/navigate_to_pose` | `nav2_msgs/action/NavigateToPose` | Relay → Nav2 action server |
| `/plan` | `nav_msgs/msg/Path` | Nav2 → visualization/recording |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Final Nav2 output → command gate |
| `/lidar_drone/stop` | `std_msgs/msg/Bool` | Scan watchdog → gate; true means block |
| `/lidar_drone/cmd_vel_checked` | `geometry_msgs/msg/Twist` | Gate → inspection only |
| `/lidar_drone/gate_status` | `std_msgs/msg/String` | Gate → inspection/recording |

The manuscript also names `/goal_pose`; the new relay uses the explicit action API instead. Map and costmap topic availability depends on the installed Nav2 configuration. Check actual topic names and types before recording.

## Reconstructed goal handling

Only finite goals in `map` with a unit quaternion are accepted. The action server must be ready. While a goal is pending or running, additional goals are rejected with a warning. The node logs completion status and never reports an aborted goal as successful. Cancellation and preemption are not implemented in this minimal relay; use a Nav2 action client for cancellation.

## Reconstructed scan watchdog

All scan angles are considered. Any finite nonnegative range at or below `stop_distance` blocks the command. Empty scans, insufficient finite in-range samples, invalid range bounds, unexpected frame IDs and scan arrival timeouts also block. Positive infinity counts as unknown, so an open field with many no-return rays may cause conservative stopping. That behavior is intentional and needs review against the actual driver's semantics.

The default threshold is 1 m from the **sensor**, not the propeller boundary. Tune it using sensor offset, complete vehicle envelope, braking distance and delays. The code does not check angular coverage or compensate for sensor occlusion.

## Reconstructed command gate

The gate runs at 20 Hz. It outputs zero if the stop heartbeat is missing/stale, an obstacle is reported, the command is missing/stale, or a command contains a nonfinite component. Otherwise it caps the planar vector magnitude and yaw rate. Other axes are suppressed. Defaults are 0.3 m/s and 0.3 rad/s, selected as bench examples rather than validated vehicle limits.

Steady timers and monotonic receipt times make the watchdog independent of `/clock` pauses. Receipt-time checks cannot detect historical data being replayed at a fresh rate. Process death means output stops; no software process can promise a final zero after it has been killed. Any future downstream consumer needs its own watchdog.

## Autopilot boundary — not implemented

Nav2 velocities normally describe motion in the robot's body frame. MAVROS velocity plugins have explicit message types and frame settings. ROS ENU/FLU conventions and MAVLink NED/FRD conversion must be verified using the exact installed plugin configuration. Setting `header.frame_id` alone is not proof that the plugin rotates a command.

Before adding a flight adapter, obtain the original code and confirm the FCU firmware, MAVROS version, setpoint topic/type, `mav_frame`, yaw convention, altitude behavior, mode and arming checks, stale odometry response and pilot override. Test body-forward motion at headings of 0°, 90° and 180° in SITL. Verify loss of commands, sensor failure and restart behavior before any vehicle trial.
