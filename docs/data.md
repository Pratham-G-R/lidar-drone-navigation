# Data collection and analysis

## What data exists

`data/source_manifest.csv` records the original project files with byte counts and SHA-256 digests. Photos and video are real project assets. `data/media_metadata.json` records image dimensions, video duration and technical metadata extracted from those files. These values describe files, not system performance.

Measured trajectory CSVs, ROS bags, FCU logs, map exports, timing traces and controlled test results are not yet archived. `data/raw/` and `data/maps/` therefore contain documentation only. Artificial numerical examples live only inside tests and are not experiment results.

## Capture a reproducible session

Keep an operator record for each session with:

| Field | Record |
| --- | --- |
| Identity | Session ID, operator, actual capture date/time and timezone |
| Software | OS, ROS distro, package versions, source commits, repo commit |
| Hardware | FCU firmware, sensor variant, airframe, mass, power supply |
| Geometry | Sensor transform, complete vehicle footprint, scan plane height |
| Configuration | Parameter YAML, FCU parameter export, relevant calibration |
| Environment | Indoor/outdoor, geometry, lighting, moving obstacles, wind if relevant |
| Execution | Manual/mapping/planning/autonomous mode; commanded route and intervention times |
| Ground truth | Measurement instrument, uncertainty, coordinate alignment and synchronization |
| Outcome | Completed/aborted, failure reason, log filenames, observations |

Run `tools/record_bag.sh` for the listed ROS topics. Check `ros2 bag info` afterward for duration, message counts and missing streams. Save parameters and package inventory on the ROS machine:

```bash
ros2 param dump /slam_toolbox > data/raw/slam_session_001.yaml
ros2 param dump /controller_server > data/raw/controller_session_001.yaml
dpkg-query -W 'ros-jazzy-*' > data/raw/ros_packages_session_001.txt
```

Use the actual node names from `ros2 node list`. Record FCU logs separately. The recorder does not collect every action/service transaction or all diagnostic topics; extend the topic list for the question being measured.

## CSV interface

`data/odometry_schema.csv` is a header-only schema with these columns:

| Column | Unit | Meaning |
| --- | --- | --- |
| `stamp_s` | s | Source odometry timestamp, consistent clock within one run |
| `x_m` | m | Odometry x coordinate |
| `y_m` | m | Odometry y coordinate |
| `z_m` | m | Odometry z coordinate |

Export actual pose samples from `/mavros/local_position/odom` into this schema. Screenshots do not contain the underlying pose samples. A rosbag-to-CSV exporter can be added once the actual storage format and message stream are provided.

```bash
python3 tools/analyze_odometry.py data/raw/trajectory.csv --output data/raw/trajectory_summary.json
```

The analysis rejects empty data, nonfinite values and repeated or decreasing timestamps. It computes sample count, duration, average interval rate `(N-1)/(last-first)`, maximum gap, planar odometry path length and altitude span. This is not measured position error: drift or pose jumps can inflate path length. Header timestamps measure sampling cadence, not end-to-end latency.

## Measurements still needed

Map accuracy requires a surveyed reference or measured landmarks. Goal error requires a reference endpoint in a registered coordinate frame. Replanning latency requires synchronized obstacle-detection and replacement-plan timestamps. Obstacle clearance requires measured geometry and a defined vehicle envelope. Success rate requires a stated trial count, route, failure definition and all outcomes, including aborted trials. CPU/RAM values require a timestamped monitor log and specified workload.

Base performance charts and quantitative tables on recorded samples, with the corresponding logs and measurement method available.
