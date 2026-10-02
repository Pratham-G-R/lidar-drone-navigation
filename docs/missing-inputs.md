# Inputs needed from the project team

As of 2026-10-02, the user does not have the original implementation/configuration and experimental logs available and plans to add them manually later. Publication can proceed with these gaps documented. The user recalls manual flight; no autonomous-flight claim is made.

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
- Per-clip log confirmation of the user-recalled manual flight and the mapping/planning state.
- Any measured accuracy, loop rate, processing load, latency, clearance, goal error or repeated-trial records.

## Repository and credit details

- Destination confirmed: https://github.com/Pratham-G-R/lidar-drone-navigation (public at initial upload).
- Confirm title, author order, affiliations, contributor roles and a maintainer contact.
- Select a code license and clarify reuse rights for shared team photographs/video/manuscript.

The package can be reviewed now. These missing inputs are explicitly tracked rather than silently filled with guessed experiment settings or fabricated measurements.
