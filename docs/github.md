# Repository maintenance

Repository: https://github.com/Pratham-G-R/lidar-drone-navigation

The user selected this public repository for the initial project upload on 2026-10-02. It contains the supplied media and source material, reconstructed support code and documentation. The user recalls manual flight and plans to add the original code, configuration and experimental records later.

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

Original photos, video and the manuscript remain preserved. None of the media is labelled proof of autonomous flight.
