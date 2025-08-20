"""
Test suite for the pathway progress models.
"""

from app.models.pathway import PathwayProgress


def test_create_pathway_progress(db_session, patient, pathway):
    """
    Ensure a PathwayProgress can be created and retrieved.
    """
    progress = PathwayProgress(
        patient_id=patient.id,
        pathway_id=pathway.id,
        progress_percent=50
    )
    db_session.add(progress)
    db_session.commit()

    fetched = db_session.query(PathwayProgress).first()
    assert fetched.progress_percent == 50
