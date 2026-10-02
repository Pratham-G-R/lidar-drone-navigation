# Primary technical references

Official project documentation consulted during preparation on 2026-10-02. Online main/rolling pages can change; confirm behavior against the versions installed on the Pi.

| Reference | Why it matters |
| --- | --- |
| [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/) | Installation, package structure and ROS interfaces |
| [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) | Map generation, frame requirements and launch/config files |
| [Online asynchronous launch](https://github.com/SteveMacenski/slam_toolbox/blob/ros2/launch/online_async_launch.py) | `slam_params_file` launch argument |
| [Nav2 Iron to Jazzy migration](https://docs.nav2.org/rolling/configuration_and_development/migration_guides/iron/Iron/) | Optional stamped command support in Jazzy |
| [Nav2 Jazzy velocity smoother](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/configuring_velocity_smoother/) | Final velocity output and message-type configuration |
| [MAVROS velocity plugin](https://mavros.readthedocs.io/en/latest/plugins/std/setpoint_velocity/) | Stamped/unstamped subscribers and explicit MAVLink frame parameter |
| [ArduPilot Guided commands](https://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html) | Velocity targets, coordinate frames and command behavior |
| [RPLidar ROS package index](https://index.ros.org/p/rplidar_ros/) | ROS driver provenance and launch-name differences |
| [SLAMTEC ROS 2 driver](https://github.com/Slamtec/sllidar_ros2) | Alternative official driver; not assumed to be the original installed package |

The paper's five example bibliography entries are template placeholders. They are preserved only in the unmodified source material and are not presented here as real supporting literature. This repository does not claim publication, peer review or a DOI.
