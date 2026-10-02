import tempfile
from pathlib import Path
import unittest
from tools.analyze_odometry import analyze


class AnalysisTests(unittest.TestCase):
    def evaluate(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'trajectory.csv'; p.write_text(text)
            return analyze(p)

    def test_known_geometry(self):
        # Artificial test geometry, never experimental data.
        r = self.evaluate('stamp_s,x_m,y_m,z_m\n0,0,0,1\n1,3,4,1\n2,6,8,2\n')
        self.assertEqual(r['planar_odometry_path_length_m'], 10.)
        self.assertEqual(r['average_interval_rate_hz'], 1.)

    def test_reject_bad_data(self):
        for text in ('stamp_s,x_m,y_m,z_m\n',
                     'stamp_s,x_m,y_m,z_m\n0,0,0,0\n0,1,1,1\n',
                     'stamp_s,x_m,y_m,z_m\n0,0,0,0\n1,nan,1,1\n'):
            with self.subTest(text=text), self.assertRaises(ValueError): self.evaluate(text)
