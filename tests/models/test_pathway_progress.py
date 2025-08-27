"""
Test suite for the pathway progress models.
"""

from app.models.pathway import PathwayProgress


def test_create_pathway_progress(pathway_progress):
    """
    Ensure a PathwayProgress can be retrieved and its fields are correct.
    """
    fetched = pathway_progress

    # Check patient association
    assert fetched.patient_id is not None

    # Check progress values
    assert fetched.steps_total == 5
    assert fetched.steps_completed == 0

    # Check status and outcome enums
    assert fetched.status == fetched.status.ACTIVE
    assert fetched.outcome == fetched.outcome.UNKNOWN

    # Check boolean flags
    assert not fetched.readmitted
    assert not fetched.had_complication
    assert not fetched.had_relapse
