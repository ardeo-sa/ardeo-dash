from sqlalchemy.orm import Session
from collections import defaultdict
from datetime import datetime
import pandas as pd

from app.models.primary import pathway_form_map
from app.models.primary.Referrals import Referrals
from app.models.primary.Subject import Subject
from app.models.primary.episode import Episode
from app.models.primary.afFormData import AfFormData
from app.models.primary.PathwayForms import PathwayForms
from app.models.primary.Pathway import pathway_formsummary_map_order
from app.models.primary.PathwayFormSummaryMap import PathwayFormSummaryMap


class pathway_Service:
    """
    Service class providing pathway analytics functions, such as calculating
    pathway adherence rates and days to treatment based on database records.
    """

    def __init__(self, db: Session):
        """
        Initialize the service with a SQLAlchemy database session.

        Args:
            db (Session): SQLAlchemy session object for database access.
        """
        self.db = db

    def pathway_adherence_rate(self):
        """
        Calculates the adherence rate to mandatory pathway forms for each episode.

        The function computes:
        - Total number of mandatory forms per episode.
        - Number of submitted mandatory forms.
        - Adherence percentage = (submitted / total) * 100.

        Returns:
            pd.DataFrame: A DataFrame with episode ID, subject ID, total mandatory forms,
                          submitted forms, and adherence percentage.
        """
        # Load data
        episodes = self.db.query(Episode).join(Subject).all()
        referrals = self.db.query(Referrals).all()
        af_forms = self.db.query(AfFormData).all()
        pfm = self.db.query(pathway_form_map).all()
        pathway_forms = self.db.query(PathwayForms).filter(PathwayForms.is_mandatory == True).all()

        # Create lookups
        pf_map = defaultdict(set)
        for pfmap in pfm:
            pf_map[pfmap.pathway_id].add(pfmap.formsSet_KEY)

        mandatory_forms = {pf.pathway_form_id: pf.afobject_id for pf in pathway_forms}

        submitted_forms_map = defaultdict(set)
        for af in af_forms:
            if af.afo_id:
                submitted_forms_map[af.episode_id].add(af.afo_id)

        referral_map = defaultdict(list)
        for rd in referrals:
            referral_map[rd.episode_id].append(rd)

        results = []
        for cs in episodes:
            episode_id = cs.episode_id
            subject_id = cs.subject_id
            pathway_ids = set()

            if cs.pathway_id:
                pathway_ids.add(cs.pathway_id)
            for rd in referral_map.get(episode_id, []):
                if rd.pathway_id:
                    pathway_ids.add(rd.pathway_id)

            mandatory_filter_form_ids = set()
            for pid in pathway_ids:
                form_ids = pf_map.get(pid, set())
                for fid in form_ids:
                    ffilter_id = mandatory_forms.get(fid)
                    if ffilter_id:
                        mandatory_filter_form_ids.add(ffilter_id)

            submitted_forms = submitted_forms_map.get(episode_id, set())
            total = len(mandatory_filter_form_ids)
            submitted = len(mandatory_filter_form_ids & submitted_forms)
            adherence = round((submitted * 100.0 / total), 2) if total > 0 else None

            results.append({
                "episode_id": episode_id,
                "subject_id": subject_id,
                "total_mandatory_forms": total,
                "submitted_mandatory_forms": submitted,
                "adherence_percentage": adherence
            })

        return pd.DataFrame(results)

    def days_to_treatment(self):
        """
        Calculates the number of days between the treatment start (first relevant form submission)
        and the episode start for each episode with a defined start date.

        The treatment start date is determined based on the lowest child index form in
        the pathway's summary form order.

        Returns:
            pd.DataFrame: A DataFrame with subject ID, episode ID, episode start date,
                          treatment start date, and days to treatment start.
        """
        episodes = self.db.query(Episode).filter(Episode.start_date.isnot(None)).all()
        referrals = self.db.query(Referrals).all()
        pfmo_all = self.db.query(pathway_formsummary_map_order).all()
        pfsm_all = self.db.query(PathwayFormSummaryMap).all()
        af_forms = self.db.query(AfFormData).all()

        min_index_map = {}
        for p in pfmo_all:
            if p.pathway_id not in min_index_map or p.child_index < min_index_map[p.pathway_id][1]:
                min_index_map[p.pathway_id] = (p.pathway_form_summary_id, p.child_index)

        summary_map = {pfs.pathway_form_summary_id: pfs.afobject_id for pfs in pfsm_all}

        aff_instance_map = defaultdict(dict)
        for af in af_forms:
            if af.afo_id:
                aff_instance_map[af.episode_id][af.afo_id] = af.creation_date

        referral_map = defaultdict(list)
        for rd in referrals:
            referral_map[rd.episode_id].append(rd)

        records = []
        for cs in episodes:
            episode_id = cs.episode_id
            subject_id = cs.subject_id
            episode_start = cs.start_date

            pathway_ids = set()
            if cs.pathway_id:
                pathway_ids.add(cs.pathway_id)
            for rd in referral_map.get(episode_id, []):
                if rd.pathway_id:
                    pathway_ids.add(rd.pathway_id)

            filter_form_ids = []
            for pid in pathway_ids:
                if pid in min_index_map:
                    pf_summary_id = min_index_map[pid][0]
                    filter_id = summary_map.get(pf_summary_id)
                    if filter_id:
                        filter_form_ids.append(filter_id)

            aff_instances = aff_instance_map.get(episode_id, {})
            treatment_dates = [aff_instances.get(fid) for fid in filter_form_ids if aff_instances.get(fid)]

            if treatment_dates:
                treatment_start = min(treatment_dates)
                days_to_treatment = (episode_start - treatment_start).days
                records.append({
                    "subject_id": subject_id,
                    "episode_id": episode_id,
                    "episode_start": episode_start,
                    "treatment_start_date": treatment_start,
                    "days_to_treatment_start": days_to_treatment
                })

        return pd.DataFrame(records)
