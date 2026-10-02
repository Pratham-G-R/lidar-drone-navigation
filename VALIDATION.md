# Validation record

Prepared 2026-10-02.

| Check | Outcome |
| --- | --- |
| ROS-independent unit tests | 14 tests passed |
| Python syntax compilation | Passed for package, tools and launch file |
| Shell recorder syntax | Passed `bash -n` |
| Original asset hashes | 18 copied sources match their input bytes |
| Internal Markdown links | All local file targets exist |
| ROS 2 / colcon integration | Not run; ROS is unavailable in this environment |
| Hardware, flight and original experiment reproduction | Not run |

Tests cover scan validity, obstacle decisions, command/safety timeout handling, speed limits, clock reversal and descriptive CSV analysis. Original flight code and tuned configuration remain missing. The CI workflow repeats offline tests and syntax compilation; it is not a ROS or flight integration test.
