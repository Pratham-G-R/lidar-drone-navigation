# Repository maintenance

Repository: https://github.com/Pratham-G-R/lidar-drone-navigation

This repository contains project media, research notes, reconstructed support code and documentation. Original code, tuned configurations and experimental records will be added when recovered. Field footage is documented as manual flight based on the maintainer's recollection.

## Add the original implementation later

Clone the repository using your normal GitHub credentials. Add recovered scripts and tuned YAML under `original_implementation/`, together with a README identifying their source machine, capture date, software versions and original paths. Keep the reconstructed package distinguishable until the original implementation is reviewed and integrated.

For ROS bags and FCU logs, preserve a session ID, metadata and checksums. `data/raw/` and `data/maps/` are ignored by default to prevent accidental addition of large recordings. Explicitly add reviewed small maps with `git add -f`, or host larger datasets separately and commit their links and hashes. Never commit credentials.

## Future contributions

Run the offline checks before pushing:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q lidar_drone launch tools
```

The CI workflow checks only Python logic and syntax. Record ROS/Jazzy integration and vehicle validation separately. Confirm author details and license selection before representing this as a licensed open-source release.

Keep original media intact and identify each recording by session and flight mode. The manuscript remains an unfinished draft until its references, captions and template remnants are corrected.
