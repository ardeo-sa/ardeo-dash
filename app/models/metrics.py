"""
This module defines SQLAlchemy ORM models for tracking various healthcare metrics within the system.

It includes the following models:

1. `PatientMetrics`: Tracks patient-specific metrics such as the average length of stay and the total admission count.
2. `OperationalMetrics`: Records operational metrics related to healthcare services, such as patient satisfaction and staff availability.
3. `MDTMetrics`: Focuses on metrics related to Multidisciplinary Team (MDT) meetings, including meeting attendance, action completion, and wait times.
4. `PathwayMetrics`: Monitors metrics associated with patient pathways, including treatment timelines, readmission rates, and no-show rates.

Each model maps to a respective table in the database, and the attributes of each class reflect the key metrics tracked for monitoring and improving healthcare services.
"""

from sqlalchemy import Column, Integer, Float, Date, String

from app.database.metrics import Base


class PatientMetrics(Base):
    """
       Represents the metrics related to patients' healthcare journey.

       Attributes:
           id (int): Primary key for the patient metrics record.
           date (Date): The date on which the metrics were recorded.
           avg_length_of_stay (float): The average length of stay for patients, in days.
           admission_count (int): The number of admissions recorded for patients on the given date.
    """
    __tablename__ = "patient_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    avg_length_of_stay = Column(Float)
    admission_count = Column(Integer)


class OperationalMetrics(Base):
    """
        Represents operational metrics, focusing on various metrics tracked within the healthcare facility.

        Attributes:
            id (int): Primary key for the operational metrics record.
            date (Date): The date on which the operational metrics were recorded.
            metric_name (str): The name of the specific operational metric (e.g., 'Patient Satisfaction', 'Staff Availability').
            value (float): The value or result of the operational metric being tracked.
            unit (str): The unit of measurement for the metric (e.g., 'percent', 'count', 'hours').
    """
    __tablename__ = "operational_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    metric_name = Column(String)
    value = Column(Float)
    unit = Column(String)


class MDTMetrics(Base):
    """
        Represents metrics related to Multidisciplinary Team (MDT) meetings.

        Attributes:
            id (int): Primary key for the MDT metrics record.
            date (Date): The date on which the MDT metrics were recorded.
            meeting_count (int): The number of MDT meetings held on the given date.
            avg_attendance (float): The average attendance for MDT meetings, as a percentage.
            avg_wait_time (float): The average wait time for cases to be discussed in MDT meetings, in days.
            action_completion_rate (float): The percentage of actions completed after MDT meetings.
    """
    __tablename__ = "mdt_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    meeting_count = Column(Integer, nullable=False)
    avg_attendance = Column(Float, nullable=False)
    avg_wait_time = Column(Float, nullable=False)  # in days
    action_completion_rate = Column(Float, nullable=False)  # percent


class PathwayMetrics(Base):
    """
       Represents metrics related to patient pathways, including treatment and readmission rates.

       Attributes:
           id (int): Primary key for the pathway metrics record.
           date (Date): The date on which the pathway metrics were recorded.
           avg_admission_to_treatment_days (float): The average number of days from admission to treatment.
           readmission_rate_30d (float): The readmission rate within 30 days, as a percentage.
           no_show_rate (float): The percentage of patients who did not show up for their scheduled appointments.
    """
    __tablename__ = "pathway_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    avg_admission_to_treatment_days = Column(Float, nullable=False)
    readmission_rate_30d = Column(Float, nullable=False)
    no_show_rate = Column(Float, nullable=False)  # percent
