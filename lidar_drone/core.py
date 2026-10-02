"""ROS-independent checks for the reconstructed bench prototype."""
from dataclasses import dataclass
import math


def scan_blocked(ranges, range_min, range_max, stop_distance, min_valid_fraction):
    """Fail closed on missing/invalid scans. +inf is unknown, not proven clear."""
    if not ranges or not (0 <= range_min < range_max < math.inf):
        return True
    valid = [r for r in ranges if math.isfinite(r) and range_min <= r <= range_max]
    too_close = any(math.isfinite(r) and 0 <= r <= stop_distance for r in ranges)
    return too_close or len(valid) / len(ranges) < min_valid_fraction


def planar_command(values, max_speed, max_yaw_rate):
    """Validate six Twist components, clamp planar speed, suppress other axes."""
    if len(values) != 6 or not all(math.isfinite(v) for v in values):
        return None
    x, y, _, _, _, yaw = values
    norm = math.hypot(x, y)
    if norm > max_speed:
        x, y = x * max_speed / norm, y * max_speed / norm
    return (x, y, max(-max_yaw_rate, min(max_yaw_rate, yaw)))


@dataclass
class CommandGate:
    command_timeout: float = 0.5
    safety_timeout: float = 0.3
    max_speed: float = 0.3
    max_yaw_rate: float = 0.3
    command: tuple | None = None
    command_time: float | None = None
    safety_time: float | None = None
    blocked: bool = True

    def receive_command(self, values, now):
        self.command = planar_command(values, self.max_speed, self.max_yaw_rate)
        self.command_time = now

    def receive_safety(self, blocked, now):
        self.blocked, self.safety_time = bool(blocked), now

    def output(self, now):
        if self.safety_time is None or not 0 <= now - self.safety_time <= self.safety_timeout:
            return (0.0, 0.0, 0.0), 'safety_stale'
        if self.blocked:
            return (0.0, 0.0, 0.0), 'obstacle_or_invalid_scan'
        if self.command_time is None or not 0 <= now - self.command_time <= self.command_timeout:
            return (0.0, 0.0, 0.0), 'command_stale'
        if self.command is None:
            return (0.0, 0.0, 0.0), 'invalid_command'
        return self.command, 'clear'
