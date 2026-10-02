# Evidence catalogue

The source filenames contain `20261001`, but a filename is not verification of the capture date. The original files are preserved byte-for-byte. `data/source_manifest.csv` provides their paths, sizes and SHA-256 digests. README previews are separately re-encoded derivatives.

## Photographs

| Original filename | Visible content | What it supports |
| --- | --- | --- |
| [IMG-20261001-WA0018.jpg](../assets/photos/IMG-20261001-WA0018.jpg) | Photographed visualization with mapped-looking structure and colored traces | Qualitative visualization record; trace identity and scale unverified |
| [IMG-20261001-WA0019.jpg](../assets/photos/IMG-20261001-WA0019.jpg) | Wider view of a similar visualization | Qualitative display record, not exported ground truth |
| [IMG-20261001-WA0020.jpg](../assets/photos/IMG-20261001-WA0020.jpg) | Close view of mapped-looking geometry and traces | Qualitative visualization record |
| [IMG-20261001-WA0027.jpg](../assets/photos/IMG-20261001-WA0027.jpg) | Sensor and companion-computer stack on airframe | Physical integration |
| [IMG-20261001-WA0028.jpg](../assets/photos/IMG-20261001-WA0028.jpg) | Drone at outdoor field near dusk | Field context; flight mode unknown |
| [IMG-20261001-WA0029.jpg](../assets/photos/IMG-20261001-WA0029.jpg) | Wiring and illuminated onboard display | Hardware detail; readings not transcribed as measurements |
| [IMG-20261001-WA0030.jpg](../assets/photos/IMG-20261001-WA0030.jpg) | LiDAR mounted above companion computer | Sensor/compute arrangement |
| [IMG-20261001-WA0032.jpg](../assets/photos/IMG-20261001-WA0032.jpg) | Laptop visualization with a grid and sparse objects | UI state; not proof of successful SLAM |
| [IMG-20261001-WA0033.jpg](../assets/photos/IMG-20261001-WA0033.jpg) | Laptop visualization with dense scan/map-like structure | Qualitative perception display |
| [IMG-20261001-WA0035.jpg](../assets/photos/IMG-20261001-WA0035.jpg) | Similar grid display to WA0032 | Possible related/compressed view; retained independently |
| [IMG-20261001-WA0036.jpg](../assets/photos/IMG-20261001-WA0036.jpg) | Similar perception display to WA0033 | Possible related/compressed view; not an independent trial |
| [IMG-20261001-WA0039.jpg](../assets/photos/IMG-20261001-WA0039.jpg) | Drone in field near dusk | Field context |
| [IMG-20261001-WA0041.jpg](../assets/photos/IMG-20261001-WA0041.jpg) | Drone and laptop on grass | Field equipment setup |

## Videos

Inspection used sampled frames at 10%, 50% and 90% of each video's duration. Audio was not transcribed, and the full videos were not scored frame-by-frame. Duration is extracted from container metadata.

| File | Duration | Sampled content |
| --- | --- | --- |
| [VID-20261001-WA0037.mp4](../assets/videos/VID-20261001-WA0037.mp4) | 28.092 s | Ground-control telemetry and map display |
| [VID-20261001-WA0031.mp4](../assets/videos/VID-20261001-WA0031.mp4) | 55.699 s | Laptop visualization and outdoor field views |
| [VID-20261001-WA0038.mp4](../assets/videos/VID-20261001-WA0038.mp4) | 38.034 s | Drone at multiple apparent positions above the field |

On 2026-10-02, the user clarified that the flight was manual as far as they recall. These clips are therefore catalogued as manual-flight project evidence, with exact per-clip mode pending logs. They do not establish autonomous waypoint execution, avoidance response time or repeated-trial success. Original ROS bags, map exports and flight logs will be added by the user when available.

## Written sources

- [Original terminal notes](../source_material/Stupid-Linux-GPS-only.txt): launch commands, serial settings, script names and absolute YAML paths. No Python implementations or YAML content are included.
- [Original manuscript](../source_material/Lidar-drone-paper-1.docm): supplied draft, preserved unchanged. No macros were executed. It includes template references and an unfinished figure caption.
- [Extracted manuscript text](../source_material/manuscript-extracted.txt): search-friendly text extraction; layout and images omitted.

## Claims and evidence gaps

| Claim | Current status | Evidence needed |
| --- | --- | --- |
| LiDAR and companion computer integrated on a drone | Visually supported | Wiring, component and mounting records for reproducibility |
| GPS-assisted map generation | Reported; display evidence is qualitative | Bag with scans, odometry, TF and map; exported map |
| Costmap inflation and global planning | Reported; overlays visible without verified topic identity | `/plan`, costmaps, goal and parameter files from the same run |
| Autonomous dynamic obstacle avoidance | Not established by the attachments | Synchronized scan/command/FCU logs, obstacle protocol and intervention record |
| HDOP above about 1.5 causes observed drift artifacts | Manuscript observation only | Synchronized GPS quality, odometry and map logs |
| Odometry below about 5 Hz degrades yaw mapping | Manuscript observation only | Controlled rate/turn experiments and recorded streams |
| GPS-denied RF2O operation | Proposed | Implementation, estimator integration and validation |
| LiDAR-free multi-drone use of shared maps | Proposed | Localization/alignment method and live obstacle strategy |

The manuscript's use of “safe” and “collision-free” is not converted into an independently validated guarantee. No numerical performance table has been fabricated from its narrative.
