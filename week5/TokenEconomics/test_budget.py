
import unittest

from budget import FeatureBudget


class TestFeatureBudget(unittest.TestCase):

    def setUp(self):
        self.budget = FeatureBudget(
            requests_per_day=1000,
            avg_input_tokens=1000,
            avg_output_tokens=500,
            input_price_per_million=1.0,
            output_price_per_million=2.0,
            peak_requests_per_minute=10,
            rpm_limit=20,
            tpm_limit=20000,
            monthly_budget_usd=100,
            daily_budget_usd=5,
            safety_margin_percent=20,
        )

    def test_cost_estimate(self):
        result = self.budget.calculate()

        self.assertAlmostEqual(result["daily_cost_usd"], 2.0)
        self.assertAlmostEqual(result["monthly_cost_usd"], 60.0)

    def test_capacity_passes(self):
        result = self.budget.calculate()

        self.assertTrue(result["checks"]["rpm_ok"])
        self.assertTrue(result["checks"]["tpm_ok"])

    def test_rpm_limit_fails(self):
        self.budget.rpm_limit = 5
        result = self.budget.calculate()

        self.assertFalse(result["checks"]["rpm_ok"])
        self.assertEqual(result["recommendation"], "REVISE")

    def test_monthly_budget_fails(self):
        self.budget.monthly_budget_usd = 50
        result = self.budget.calculate()

        self.assertFalse(result["checks"]["monthly_budget_ok"])
        self.assertEqual(result["recommendation"], "REVISE")


if __name__ == "__main__":
    unittest.main()
