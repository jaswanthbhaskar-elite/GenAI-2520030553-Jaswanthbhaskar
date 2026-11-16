
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class FeatureBudget:
    requests_per_day: int
    avg_input_tokens: int
    avg_output_tokens: int
    input_price_per_million: float
    output_price_per_million: float
    peak_requests_per_minute: int
    rpm_limit: int
    tpm_limit: int
    monthly_budget_usd: float
    daily_budget_usd: float
    safety_margin_percent: float = 20.0

    @classmethod
    def from_env(cls):
        return cls(
            requests_per_day=int(os.getenv("REQUESTS_PER_DAY", 2000)),
            avg_input_tokens=int(os.getenv("AVG_INPUT_TOKENS", 1200)),
            avg_output_tokens=int(os.getenv("AVG_OUTPUT_TOKENS", 300)),
            input_price_per_million=float(os.getenv("INPUT_PRICE_PER_MILLION", 0.30)),
            output_price_per_million=float(os.getenv("OUTPUT_PRICE_PER_MILLION", 1.20)),
            peak_requests_per_minute=int(os.getenv("PEAK_REQUESTS_PER_MINUTE", 30)),
            rpm_limit=int(os.getenv("RPM_LIMIT", 60)),
            tpm_limit=int(os.getenv("TPM_LIMIT", 100000)),
            monthly_budget_usd=float(os.getenv("MONTHLY_BUDGET_USD", 50)),
            daily_budget_usd=float(os.getenv("DAILY_BUDGET_USD", 2)),
            safety_margin_percent=float(os.getenv("SAFETY_MARGIN_PERCENT", 20)),
        )

    def calculate(self):
        if min(
            self.requests_per_day,
            self.avg_input_tokens,
            self.avg_output_tokens,
            self.peak_requests_per_minute,
            self.safety_margin_percent,
        ) < 0:
            raise ValueError("Usage assumptions cannot be negative.")

        input_tokens_day = self.requests_per_day * self.avg_input_tokens
        output_tokens_day = self.requests_per_day * self.avg_output_tokens
        total_tokens_day = input_tokens_day + output_tokens_day

        input_cost_day = (
            input_tokens_day * self.input_price_per_million / 1_000_000
        )
        output_cost_day = (
            output_tokens_day * self.output_price_per_million / 1_000_000
        )

        daily_cost = input_cost_day + output_cost_day
        monthly_cost = daily_cost * 30

        margin = 1 + self.safety_margin_percent / 100

        peak_tpm = (
            self.peak_requests_per_minute
            * (self.avg_input_tokens + self.avg_output_tokens)
            * margin
        )
        peak_rpm = self.peak_requests_per_minute * margin

        checks = {
            "rpm_ok": peak_rpm <= self.rpm_limit,
            "tpm_ok": peak_tpm <= self.tpm_limit,
            "daily_budget_ok": daily_cost * margin <= self.daily_budget_usd,
            "monthly_budget_ok": monthly_cost * margin <= self.monthly_budget_usd,
        }

        return {
            "input_tokens_day": input_tokens_day,
            "output_tokens_day": output_tokens_day,
            "total_tokens_day": total_tokens_day,
            "daily_cost_usd": daily_cost,
            "monthly_cost_usd": monthly_cost,
            "peak_rpm_with_margin": peak_rpm,
            "peak_tpm_with_margin": peak_tpm,
            "checks": checks,
            "recommendation": "GO" if all(checks.values()) else "REVISE",
        }


def main():
    budget = FeatureBudget.from_env()
    result = budget.calculate()

    print("\n=== LLM FEATURE BUDGET REPORT ===")
    print(f"Input tokens/day: {result['input_tokens_day']:,}")
    print(f"Output tokens/day: {result['output_tokens_day']:,}")
    print(f"Total tokens/day: {result['total_tokens_day']:,}")
    print(f"Estimated daily cost: ${result['daily_cost_usd']:.4f}")
    print(f"Estimated monthly cost: ${result['monthly_cost_usd']:.2f}")
    print(f"Peak RPM with margin: {result['peak_rpm_with_margin']:.1f}")
    print(f"Peak TPM with margin: {result['peak_tpm_with_margin']:.0f}")

    print("\n=== LIMIT CHECKS ===")
    for name, passed in result["checks"].items():
        print(f"{name}: {'PASS' if passed else 'REVIEW'}")

    print(f"\nRECOMMENDATION: {result['recommendation']}")


if __name__ == "__main__":
    main()
