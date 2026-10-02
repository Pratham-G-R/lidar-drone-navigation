import math
import unittest
from lidar_drone.core import CommandGate, scan_blocked


class ScanTests(unittest.TestCase):
    def test_clear(self):
        self.assertFalse(scan_blocked([2.,3.], .15, 12., 1., .5))

    def test_hazard_any_direction(self):
        self.assertTrue(scan_blocked([4.,.9,8.], .15, 12., 1., .5))

    def test_invalid_and_empty(self):
        for scan in ([], [math.nan], [math.inf], [-1.], [20.], [0.]):
            with self.subTest(scan=scan):
                self.assertTrue(scan_blocked(scan, .15, 12., 1., .5))

    def test_insufficient_coverage(self):
        self.assertTrue(scan_blocked([3.,math.nan,math.nan], .15, 12., 1., .5))


class GateTests(unittest.TestCase):
    def setUp(self): self.gate = CommandGate()

    def ready(self):
        self.gate.receive_safety(False, 1.)
        self.gate.receive_command((.1,.2,0.,0.,0.,.1), 1.)

    def test_startup_is_stopped(self):
        self.assertEqual(self.gate.output(0.)[0], (0.,0.,0.))

    def test_clear(self):
        self.ready()
        self.assertEqual(self.gate.output(1.1)[0], (.1,.2,.1))

    def test_stop_priority(self):
        self.ready(); self.gate.receive_safety(True, 1.1)
        self.assertEqual(self.gate.output(1.1)[0], (0.,0.,0.))

    def test_safety_death(self):
        self.ready()
        self.assertEqual(self.gate.output(1.4)[1], 'safety_stale')

    def test_command_death(self):
        self.ready(); self.gate.receive_safety(False, 1.6)
        self.assertEqual(self.gate.output(1.6)[1], 'command_stale')

    def test_invalid_command_replaces_previous(self):
        self.ready(); self.gate.receive_command((math.nan,0,0,0,0,0),1.1)
        self.assertEqual(self.gate.output(1.1)[1], 'invalid_command')

    def test_magnitude_limits_and_planar_axes(self):
        self.ready(); self.gate.receive_command((3,4,7,8,9,10),1.1)
        x,y,yaw = self.gate.output(1.1)[0]
        self.assertAlmostEqual(math.hypot(x,y), .3)
        self.assertEqual(yaw,.3)

    def test_backward_clock(self):
        self.ready()
        self.assertEqual(self.gate.output(.9)[1], 'safety_stale')


if __name__ == '__main__': unittest.main()
