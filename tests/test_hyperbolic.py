import unittest
from curve_memory.hyperbolic import pi_a_over_pi, validate_hyperbolic_params

class TestHyperbolic(unittest.TestCase):
    def test_standard(self):
        self.assertAlmostEqual(pi_a_over_pi(1.0, 1.0), 1.1752, places=4)

    def test_zero_cases(self):
        self.assertEqual(pi_a_over_pi(0.0, 1.0), 1.0)
        self.assertEqual(pi_a_over_pi(1.0, 0.0), 1.0)

    def test_validation(self):
        valid, _ = validate_hyperbolic_params(1.0, 1.0)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
