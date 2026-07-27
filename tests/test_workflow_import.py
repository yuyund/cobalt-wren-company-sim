from company_sim.workflow import simulate_company


def test_native_workflow_is_exposed() -> None:
    assert simulate_company.name == "company.simulation"
