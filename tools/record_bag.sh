#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo 'Usage: bash tools/record_bag.sh NEW_BAG_DIRECTORY' >&2
  exit 2
fi
ros2 bag record -o "$1" --topics \
  /scan /tf /tf_static /mavros/local_position/odom /mavros/state \
  /mavros/global_position/global /map /map_metadata /plan \
  /global_costmap/costmap /local_costmap/costmap /cmd_vel \
  /lidar_drone/cmd_vel_checked /lidar_drone/stop /lidar_drone/gate_status
