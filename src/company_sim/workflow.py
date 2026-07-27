"""Cobalt Wren Native workflow for the company simulation."""

from __future__ import annotations

from collections.abc import Mapping

from cobalt_wren.native import NativeWorkflowContext, workflow

from .company import build_default_company


@workflow("company.simulation")
async def simulate_company(
    ctx: NativeWorkflowContext,
    request: Mapping[str, object],
) -> dict[str, object]:
    customer = str(request.get("customer", "external-customer"))
    goal = str(request.get("request", ""))
    if not goal.strip():
        raise ValueError("request is required")

    company = build_default_company()
    result = await ctx.step(
        "run-company",
        lambda: company.run_customer_request(customer=customer, request=goal),
    )
    await ctx.progress.update(
        current=result.rounds,
        total=result.rounds,
        message="Company simulation completed",
    )
    ctx.metric.record("company.messages", len(result.transcript), unit="message")
    ctx.metric.record("company.decisions", len(result.decisions), unit="decision")
    return {
        "status": result.status,
        "correlation_id": result.correlation_id,
        "rounds": result.rounds,
        "customer_response": result.customer_response,
        "transcript": [
            {
                "sender": message.sender,
                "recipient": message.recipient,
                "content": message.content,
                "hop": message.hop,
            }
            for message in result.transcript
        ],
        "departments": [decision.department for decision in result.decisions],
    }
