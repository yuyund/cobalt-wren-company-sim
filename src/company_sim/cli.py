"""Command-line entry point."""

from __future__ import annotations

import argparse
import json

from .company import build_default_company


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the company simulation.")
    parser.add_argument("--customer", default="external-customer")
    parser.add_argument("--request", required=True)
    args = parser.parse_args()

    result = build_default_company().run_customer_request(
        customer=args.customer,
        request=args.request,
    )
    print(
        json.dumps(
            {
                "status": result.status,
                "correlation_id": result.correlation_id,
                "rounds": result.rounds,
                "customer_response": result.customer_response,
                "departments": [decision.department for decision in result.decisions],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if result.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
