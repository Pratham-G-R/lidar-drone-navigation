# Validation and troubleshooting

## Validation status

Offline unit checks exercise obstacle decisions, invalid scans, start-up blocking, command and safety timeouts, invalid commands, planar speed limits, clock reversal and CSV analysis. Python compilation checks syntax without importing ROS. See `VALIDATION.md` for the run performed when this repository was prepared.

ROS middleware behavior, colcon installation, hardware connectivity, Nav2 lifecycle activation and flight behavior have not been verified in this environment. Passing offline tests does not establish safe flight or reproduce the original experiment.

## Bench acceptance sequence

1. Verify the expected sensor topics, types, frame IDs, timestamps and QoS.
2. Confirm exactly one publisher owns each TF edge; move the unpowered/disarmed rig and compare measured directions.
3. Verify map updates while moving the sensor through a known environment.
4. Place a stationary object at measured distances and check scan values and costmap occupancy.
5. Submit an achievable map-frame goal and inspect the generated path.
6. With the command output disconnected from any actuators, publish a test command; obstruct the scan and verify the gate becomes zero.
7. Stop the scan publisher, kill the safety node and stop command publication in separate tests. Verify both timeout paths.
8. Record and replay a ROS bag with `use_sim_time:=true` on ROS nodes and `ros2 bag play BAG --clock`. Watchdogs still use real elapsed receipt time, so replay speed affects them.

The scan and heartbeat watchdogs run on 50 ms timers. Their configured timeout is not a guaranteed real-time deadline; scheduling and system load affect response. Record observed response times rather than claiming a bound from configuration values.

## Before an autopilot bridge

Implement and test a vehicle-specific SITL adapter separately. Verify frame rotation, yaw sign, altitude behavior, command-loss handling, disarm/mode gating, emergency pilot takeover and FCU failsafes. Keep the independent downstream command timeout: death of the command gate produces silence, not a guaranteed zero command. A zero planar velocity setpoint is neither disarm nor an instantaneous physical stop.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No `/scan` | USB path, device group, driver package/launch name, variant and serial baud |
| No MAVROS odometry | FCU heartbeat, UART assignment/baud, valid estimator state, telemetry message stream |
| Frame mismatch error | Inspect both incoming odometry frame IDs; configure the source or perform an actual coordinate transform |
| TF jumps or conflicting data | Duplicate publishers, GPS/EKF resets, timestamp synchronization and odometry continuity |
| SLAM drops scans | Complete transform chain at scan time, scan frame, system clocks, CPU load and odometry rate |
| Gate remains blocked outdoors | Inspect no-return/invalid ranges; conservative valid-sample coverage rule may be blocking |
| Gate has no commands | `/cmd_vel` name, `Twist` versus `TwistStamped`, Nav2 lifecycle state, active goal |
| Goal rejected | `map` frame, valid quaternion, active prior goal and action server readiness |
| Nav2 progress aborts on bench | A stationary rig cannot fulfill movement progress requirements |
| Map looks plausible but rotates incorrectly | Measured sensor mounting transform, ENU/body conventions and frame ownership |

The manuscript reports degradation near HDOP above 1.5 and odometry below 5 Hz. These are unverified project observations, not universal thresholds. Its HDOP ≤ 1 preflight target is likewise not a complete navigation-quality check.
