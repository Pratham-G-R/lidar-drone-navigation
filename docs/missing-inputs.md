# Pending project work

The original implementation, tuned configurations and experimental logs are not yet archived in this repository. They will be added when recovered. Field flight is understood to have been manual, based on the maintainer's recollection; exact per-clip mode confirmation awaits flight logs.

## Essential for reproducing the original system

- `odom_to_tf.py`, `goal_relay.py`, `laser_safety_stop.py`, `cmd_vel_mux.py` from the Pi, with any other scripts they import.
- `mapper_params_online_async_gps.yaml` and `nav2_params_gps.yaml` from the tested machine.
- Any MAVROS launch/config files, velocity/setpoint bridge, systemd service, shell script or Foxglove layout used during the tests.
- Exact ArduPilot vehicle type/version, Pixhawk firmware target, full parameter export and UART/telemetry port assignment.
- Ubuntu version, ROS/MAVROS/Nav2/SLAM Toolbox versions, LiDAR driver branch/commit and RPLidar A1 variant.
- Measured sensor pose and vehicle dimensions including propellers; wiring/power diagram.

## Essential for experimental results

- Original ROS bags (`metadata.yaml` plus `.db3` or `.mcap` files), FCU `.BIN` logs or telemetry `.tlog` files.
- Exported `.pgm`/`.yaml` maps and any serialized SLAM pose graph.
- Trial dates, environment dimensions, target coordinates, flight/control mode, manual intervention records and pass/fail criteria.
- Per-clip log confirmation of the recalled manual flight and the mapping/planning state.
- Any measured accuracy, loop rate, processing load, latency, clearance, goal error or repeated-trial records.

## Repository and credit details

- Confirm title, author order, affiliations and contributor roles with the team.
- Select a code license and clarify reuse rights for shared team photographs/video/manuscript.

Update the setup and validation records as each item is completed. Keep recovered experiment configurations distinguishable from the current generated bench templates.
