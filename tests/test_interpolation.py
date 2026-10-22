
import sys
import unittest
from pathlib import Path

# Make the project scripts available for testing
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from interpolation_experiment import (
    linear_interpolation,
    valid_windows,
)


class TestLinearInterpolation(unittest.TestCase):
    """Verify the numerical interpolation implementation."""

    def test_midpoint(self):
        # Halfway between 20 and 24 degrees should be 22
        result = linear_interpolation(0, 20, 20, 24, 10)
        self.assertAlmostEqual(result, 22.0)

    def test_irregular_spacing(self):
        # 600 seconds is one-third of a 1800 second gap
        result = linear_interpolation(0, 20, 1800, 23, 600)
        self.assertAlmostEqual(result, 21.0)

    def test_known_endpoints(self):
        # Interpolation must reproduce the measured endpoints
        self.assertAlmostEqual(
            linear_interpolation(0, 20, 10, 30, 0), 20
        )
        self.assertAlmostEqual(
            linear_interpolation(0, 20, 10, 30, 10), 30
        )

    def test_invalid_interval(self):
        # Two readings cannot define a zero-length interval
        with self.assertRaises(ValueError):
            linear_interpolation(10, 20, 10, 25, 10)

    def test_large_gap_rejected(self):
        # The final interval is too long for validation
        data = [
            (0, 20),
            (600, 21),
            (1200, 22),
            (3000, 23),
        ]
        self.assertEqual(valid_windows(data, 1), [0])


if __name__ == "__main__":
    unittest.main()
