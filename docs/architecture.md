# Architecture and assumptions

## Hardware described by the manuscript

| Item | Role | Verification status |
| --- | --- | --- |
| Pixhawk 2.4.8 with ArduPilot | Estimation, stabilization and flight control | Reported; firmware version and parameter export missing |
| Raspberry Pi 4 Model B, reportedly 4 GB RAM | ROS 2 companion processing | Board visible; RAM, OS release and package versions need confirmation |
| RPLidar A1 over USB | Planar laser ranges | Reported and sensor assembly photographed; exact variant unknown |
| UART between Pi and FCU | MAVLink telemetry | Notes use `/dev/ttyS0:921600`; physical connector and FCU port mapping unknown |
| Drone platform | Carries the sensor and compute stack | Photographed; dimensions, mass, propulsion and propeller sweep missing |

The earlier unrelated FPV project details have not been assumed to apply to this aircraft. Wiring must be documented from this build: identify the FCU telemetry port, voltage levels, TX/RX crossing, common ground and independent regulated power. Never infer a pinout from a photograph.

## Mapping and navigation

MAVROS exposes the FCU's locally estimated pose. A single transform broadcaster supplies `odom → base_link`. A measured rigid transform connects `base_link → laser`. SLAM Toolbox consumes those transforms and scans, generates `/map`, and supplies `map → odom`. Nav2 uses the map and current laser observations in its costmaps.

The global SLAM map and a dynamic local obstacle layer serve different purposes. This project does not implement a probabilistic dynamic occupancy grid with explicit obstacle velocity tracking. The manuscript title's phrase “dynamic occupancy grids” refers here to maps/costmaps updated as observations arrive.

Nav2 is a planar navigation framework. A UAV integration must separately handle takeoff, landing, altitude control, attitude limits, flight mode, pilot override and FCU failsafes. A 2D scan cannot observe all obstacles above or below its plane; roll and pitch can make a planar interpretation inaccurate. This reconstruction does not flatten measured odometry or invent an altitude controller.

## Changes from the supplied notes

1. The original notes enable MAVROS TF and also run `odom_to_tf.py`. Use only the reconstructed broadcaster and disable MAVROS TF for this edge, or disable this broadcaster if MAVROS owns the edge.
2. The zero LiDAR mounting transform is retained only in the archive. The new setup requires a measured transform.
3. Serial access uses the normal device group instead of `chmod 666`.
4. The new goal relay submits a `NavigateToPose` action. It is not a recovered copy of the manuscript's `/goal_pose` republisher.
5. Safety is a heartbeat plus command gating on a test topic. It is not a certified emergency stop, a flight termination system or a substitute for autopilot failsafes.
6. Configurations are generated from the installed packages to avoid pretending guessed values were the tested settings. Generated Nav2 defaults still require controller, footprint and costmap review.

## Proposed extensions

RF2O could provide planar scan odometry for mapping, but GPS-denied flight also requires a suitable autopilot state estimate, height source, synchronization and EKF integration. Replacing one ROS topic alone does not establish GPS-denied flight capability.

Exported maps could be reused by another robot only with valid localization and consistent map alignment. A pre-recorded map provides no live detection of newly introduced obstacles for a vehicle without an appropriate sensor.
