#!/usr/bin/env python3
"""Adapt the locally installed Jazzy defaults; preserve their upstream metadata.

Run on the ROS machine. Outputs are bench templates, not recovered experiment settings.
"""
import argparse
import hashlib
import json
from pathlib import Path
import yaml


def configure(slam, nav, radius):
    s = slam['slam_toolbox']['ros__parameters']
    s.update(use_sim_time=False, mode='mapping', map_frame='map', odom_frame='odom',
             base_frame='base_link', scan_topic='/scan')

    def visit(value):
        if isinstance(value, dict):
            for key in list(value):
                if key == 'use_sim_time': value[key] = False
                elif key == 'enable_stamped_cmd_vel': value[key] = False
                elif key == 'odom_topic': value[key] = '/mavros/local_position/odom'
                elif key == 'robot_base_frame': value[key] = 'base_link'
                else: visit(value[key])
        elif isinstance(value, list):
            for item in value: visit(item)
    visit(nav)
    for name in ('controller_server', 'velocity_smoother', 'behavior_server'):
        if name in nav:
            nav[name]['ros__parameters']['enable_stamped_cmd_vel'] = False
    for name, frame in [('local_costmap', 'odom'), ('global_costmap', 'map')]:
        p = nav[name][name]['ros__parameters']
        p.update(global_frame=frame, robot_base_frame='base_link', robot_radius=radius)
        p.pop('footprint', None)
        for layer in p.values():
            if isinstance(layer, dict) and 'observation_sources' in layer:
                for src in layer['observation_sources'].split():
                    if src in layer:
                        layer[src]['topic'] = '/scan'
    return slam, nav


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--robot-radius', required=True, type=float,
                        help='Measured radius enclosing propeller sweep in metres')
    parser.add_argument('--output', type=Path, default=Path('config/generated'))
    args = parser.parse_args()
    if not 0 < args.robot_radius < 10:
        parser.error('robot-radius must be > 0 and < 10 metres')
    from ament_index_python.packages import get_package_share_directory
    sources = {
        'mapper_params_online_async_gps.yaml': Path(get_package_share_directory('slam_toolbox')) / 'config/mapper_params_online_async.yaml',
        'nav2_params_gps.yaml': Path(get_package_share_directory('nav2_bringup')) / 'params/nav2_params.yaml',
    }
    if args.output.exists() and any((args.output / n).exists() for n in sources):
        parser.error('Output already contains configurations; choose a new directory to avoid overwriting tuning')
    source_bytes = {n: p.read_bytes() for n, p in sources.items()}
    docs = [yaml.safe_load(b) for b in source_bytes.values()]
    slam, nav = configure(*docs, args.robot_radius)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, doc in zip(sources, (slam, nav)):
        (args.output / name).write_text('# GENERATED BENCH TEMPLATE — review before use\n' + yaml.safe_dump(doc, sort_keys=False))
    provenance = {n: {'source': str(sources[n]), 'sha256': hashlib.sha256(b).hexdigest()}
                  for n, b in source_bytes.items()}
    provenance['note'] = 'Retains installed upstream controller defaults; not tuned for aerial navigation.'
    (args.output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(args.output.resolve())


if __name__ == '__main__': main()
