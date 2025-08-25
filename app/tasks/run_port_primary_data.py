from app.tasks.worker import celery
from app.services.data_importers.port_primary_data import port_primary_data


@celery.task(name="portprimarydata")
def port_primary_data_task():
    """
    Celery task to run the primary data porting service.
    """
    return port_primary_data()
