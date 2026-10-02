#!/usr/bin/env python3
"""Describe a CSV trajectory; never infer navigation success or ground-truth error."""
import argparse
import csv
import json
import math
from pathlib import Path


def analyze(path):
    with Path(path).open(newline='') as f:
        reader = csv.DictReader(f)
        required = {'stamp_s', 'x_m', 'y_m', 'z_m'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('Expected columns: stamp_s,x_m,y_m,z_m')
        rows = [tuple(float(r[k]) for k in ('stamp_s', 'x_m', 'y_m', 'z_m')) for r in reader]
    if len(rows) < 2 or not all(math.isfinite(v) for r in rows for v in r):
        raise ValueError('At least two finite samples are required')
    dt = [b[0] - a[0] for a, b in zip(rows, rows[1:])]
    if min(dt) <= 0:
        raise ValueError('Timestamps must be strictly increasing; split clock resets into separate runs')
    path_length = sum(math.hypot(b[1]-a[1], b[2]-a[2]) for a,b in zip(rows, rows[1:]))
    duration = rows[-1][0]-rows[0][0]
    return {'samples': len(rows), 'duration_s': duration,
            'average_interval_rate_hz': (len(rows)-1)/duration,
            'max_sample_gap_s': max(dt), 'planar_odometry_path_length_m': path_length,
            'altitude_span_m': max(r[3] for r in rows)-min(r[3] for r in rows),
            'interpretation': 'Descriptive odometry only; drift affects path length. No accuracy or success claim.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv', type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        text = json.dumps(analyze(args.csv), indent=2, allow_nan=False) + '\n'
    except (ValueError, OSError, KeyError) as exc:
        p.error(str(exc))
    if args.output: args.output.write_text(text)
    else: print(text, end='')


if __name__ == '__main__': main()
