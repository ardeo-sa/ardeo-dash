from sqlalchemy.orm import Session
from collections import defaultdict
from datetime import datetime
import pandas as pd

from app.models.primary.Referrals import Referrals
from app.models.primary.Episode import Episode
from app.models.primary.Subject import Subject
from app.models.primary.AfFormData import AfFormData


class subject_Service:
    """
    Service class for analytics and metrics related to subjects and their episodes,
    including admissions, discharges, and length of stay calculations.
    """

    def __init__(self, db: Session):
        """
        Initialize the service with a SQLAlchemy session.

        Args:
            db (Session): SQLAlchemy session object for accessing the database.
        """
        self.db = db

    def _fetch_data(self):
        """
        Internal method to fetch and join episode, subject, and referral data.

        Returns:
            List[Episode]: A list of episode objects with subject and referral joins.
        """
        cs_data = (
            self.db.query(Episode)
            .join(Subject, Episode.subject_id == Subject.subject_id)
            .join(Referrals, Episode.episode_id == Referrals.episode_id)
            .all()
        )
        return cs_data

    def admissions_discharges_by_day(self):
        """
        Computes the number of admissions and discharges grouped by day.

        Returns:
            pd.DataFrame: A DataFrame containing dates with counts of admissions and discharges.
        """
        data = self._fetch_data()
        result = defaultdict(lambda: {"admission": 0, "discharge": 0})

        for cs in data:
            date_period = cs.start_date.date()
            if cs.status in ("active", "suspended"):
                result[date_period]["admission"] += 1
            elif cs.status == "discharged":
                result[date_period]["discharge"] += 1

        return pd.DataFrame([
            {"date_period": k, **v} for k, v in sorted(result.items())
        ])

    def admissions_discharges_by_week(self):
        """
        Computes the number of admissions and discharges grouped by ISO week.

        Returns:
            pd.DataFrame: A DataFrame containing week labels with counts of admissions and discharges.
        """
        data = self._fetch_data()
        result = defaultdict(lambda: {"admission": 0, "discharge": 0})

        for cs in data:
            week_period = f"{cs.start_date.year} - Week {cs.start_date.isocalendar()[1]}"
            if cs.status in ("active", "suspended"):
                result[week_period]["admission"] += 1
            elif cs.status == "discharged":
                result[week_period]["discharge"] += 1

        return pd.DataFrame([
            {"week_period": k, **v} for k, v in sorted(result.items())
        ])

    def admissions_discharges_by_month(self):
        """
        Computes the number of admissions and discharges grouped by month.

        Returns:
            pd.DataFrame: A DataFrame containing monthly periods with counts of admissions and discharges.
        """
        data = self._fetch_data()
        result = defaultdict(lambda: {"admission": 0, "discharge": 0})

        for cs in data:
            month_period = cs.start_date.strftime("%Y-%m")
            if cs.status in ("active", "suspended"):
                result[month_period]["admission"] += 1
            elif cs.status == "discharged":
                result[month_period]["discharge"] += 1

        return pd.DataFrame([
            {"month_period": k, **v} for k, v in sorted(result.items())
        ])

    def average_length_of_stay(self):
        """
        Calculates the average length of stay (in days) for discharged episodes,
        grouped by speciality.

        Length of stay is calculated as the number of days between the episode's start date
        and the latest modification date of associated form submissions (or episode modified date).

        Returns:
            pd.DataFrame: A DataFrame with specialities and their corresponding average length of stay.
        """
        episodes = self.db.query(Episode).filter(Episode.status == "discharged").all()

        af_map = defaultdict(list)
        af_list = self.db.query(AfFormData).all()
        for af in af_list:
            af_map[af.episode_id].append(af.modified_date)

        site_stays = defaultdict(list)

        for ep in episodes:
            af_dates = af_map.get(ep.episode_id, [])
            discharge_date = max(af_dates) if af_dates else ep.modified_date
            if discharge_date and ep.start_date:
                los = (discharge_date - ep.start_date).days
                site_stays[ep.speciality].append(los)

        averages = [
            {"speciality": site, "average_length_of_stay_days": sum(days) / len(days)}
            for site, days in site_stays.items() if days
        ]
        return pd.DataFrame(sorted(averages, key=lambda x: -x["average_length_of_stay_days"]))
