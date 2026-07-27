from company_sim.company import build_default_company


def test_customer_request_crosses_company_and_returns_to_customer() -> None:
    result = build_default_company().run_customer_request(
        customer="Acme Corp",
        request="We need an auditable support automation pilot in two weeks.",
    )

    assert result.status == "completed"
    assert result.customer_response is not None
    assert [decision.department for decision in result.decisions] == [
        "sales",
        "product",
        "executive",
        "engineering",
        "operations",
        "support",
    ]
    assert result.transcript[-1].recipient == "Acme Corp"
    assert result.transcript[-1].metadata["terminal"] is True


def test_each_department_uses_three_internal_agents() -> None:
    result = build_default_company().run_customer_request(
        customer="Customer",
        request="Prepare a secure rollout plan.",
    )

    assert result.decisions
    assert all(
        tuple(finding.role for finding in decision.findings)
        == ("strategy", "analysis", "execution")
        for decision in result.decisions
    )
