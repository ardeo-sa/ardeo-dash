"""
This module defines the `PathwayService` class, which provides analytics related
to clinical pathways using data from the primary database.

It includes methods to:
- Calculate pathway adherence rates by checking submission of mandatory forms
- Determine the number of days from episode start to treatment initiation

The service operates on ORM models such as `Episode`, `Referrals`, `AfFormData`, and
form mappings like `PathwayForms`, `pathway_form_map`, and `pathway_formsummary_map_order`.

Returns results as pandas DataFrames for integration with reporting or dashboard layers.
"""
import logging
from collections import defaultdict

import pandas as pd
from sqlalchemy.orm import Session
# from datetime import datetime

from app.models.primary import pathway_form_map
from app.models.primary.referrals import Referrals
from app.models.primary.subject import Subject
from app.models.primary.episode import Episode
from app.models.primary.af_form_data import AfFormData
from app.models.primary.pathway_forms import PathwayForms
from app.models.primary.pathway import pathway_formsummary_map_order
from app.models.primary.pathway_form_summary_map import PathwayFormSummaryMap

logger = logging.getLogger(__name__)


class PathwayService:
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
        logger.debug("PathwayService initialized")

    def _get_pathway_form_map(self):
        """
        Retrieve a mapping of pathway IDs to sets of form keys.

        Returns:
            defaultdict(set): Mapping pathway_id -> set of formsSet_KEY.
        """
        logger.debug("Fetching pathway_form_map")
        pfm_records = self.db.query(pathway_form_map).all()
        pf_map = defaultdict(set)
        for pf in pfm_records:
            pf_map[pf.pathway_id].add(pf.formsSet_KEY)
        logger.debug(f"Loaded {len(pf_map)} pathway form map entries")
        return pf_map

    def _get_mandatory_form_lookup(self):
        """
        Retrieve a mapping of mandatory pathway form IDs to their associated afobject IDs.

        Returns:
            dict: Mapping pathway_form_id -> afobject_id for mandatory forms.
        """
        logger.debug("Fetching mandatory forms from PathwayForms")
        mandatory_pathway_forms = self.db.query(PathwayForms).filter(
            PathwayForms.is_mandatory is True
        ).all()
        result = {
            pf.pathway_form_id: pf.afobject_id
            for pf in mandatory_pathway_forms
        }
        logger.debug(f"Loaded {len(result)} mandatory form mappings")
        return result

    def _get_submitted_forms_map(self, af_forms):
        """
        Create a mapping of episode IDs to sets of submitted afobject IDs.

        Args:
            af_forms (list): List of AfFormData records.

        Returns:
            defaultdict(set): Mapping episode_id -> set of submitted afobject_ids.
        """
        logger.debug("Building submitted forms map")
        submitted_map = defaultdict(set)
        for af in af_forms:
            if af.afo_id:
                submitted_map[af.episode_id].add(af.afo_id)
        logger.debug(f"Created submitted forms map for {len(submitted_map)} episodes")
        return submitted_map

    def _get_referral_map(self):
        """
        Create a mapping of episode IDs to lists of referral records.

        Returns:
            defaultdict(list): Mapping episode_id -> list of Referrals.
        """
        logger.debug("Fetching all Referrals")
        referrals = self.db.query(Referrals).all()
        referral_map = defaultdict(list)
        for rd in referrals:
            referral_map[rd.episode_id].append(rd)
        logger.debug(f"Created referral map for {len(referral_map)} episodes")
        return referral_map

    def _get_min_index_map(self):
        """
        Retrieve the minimum child index and corresponding form summary ID for each pathway.

        Returns:
            dict: Mapping of pathway_id to tuple (pathway_form_summary_id, child_index).
        """
        logger.debug("Fetching pathway_formsummary_map_order entries")
        pfmo_all = self.db.query(pathway_formsummary_map_order).all()
        min_map = {}
        for p in pfmo_all:
            if p.pathway_id not in min_map or p.child_index < min_map[p.pathway_id][1]:
                min_map[p.pathway_id] = (p.pathway_form_summary_id, p.child_index)
        logger.debug(f"Created min index map for {len(min_map)} pathways")
        return min_map

    def _get_summary_map(self):
        """
        Build a mapping from pathway form summary ID to afobject ID.

        Returns:
            dict: Mapping of pathway_form_summary_id to afobject_id.
        """
        logger.debug("Fetching PathwayFormSummaryMap entries")
        pfsm_all = self.db.query(PathwayFormSummaryMap).all()
        result = {pfs.pathway_form_summary_id: pfs.afobject_id for pfs in pfsm_all}
        logger.debug(f"Created summary map for {len(result)} summaries")
        return result

    def _get_aff_instance_map(self, af_forms):
        """
        Create a nested mapping of episode ID to afobject IDs and their creation dates.

        Args:
            af_forms (list): List of AfFormData records.

        Returns:
            defaultdict: Nested dict mapping episode_id -> afobject_id -> creation_date.
        """
        aff_map = defaultdict(dict)
        for af in af_forms:
            if af.afo_id:
                aff_map[af.episode_id][af.afo_id] = af.creation_date
        logger.debug(f"Created instance map for {len(aff_map)} episodes")
        return aff_map

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
        logger.info("Calculating pathway adherence rate")
        # Load data
        episodes = self.db.query(Episode).join(Subject).all()
        af_forms = self.db.query(AfFormData).all()

        # Prepare mappings
        pf_map = self._get_pathway_form_map()
        mandatory_forms = self._get_mandatory_form_lookup()
        submitted_forms_map = self._get_submitted_forms_map(af_forms)
        referral_map = self._get_referral_map()

        results = []
        for episode in episodes:
            episode_id = episode.episode_id
            subject_id = episode.subject_id

            pathway_ids = set()
            if episode.pathway_id:
                pathway_ids.add(episode.pathway_id)
            for referral in referral_map.get(episode_id, []):
                if referral.pathway_id:
                    pathway_ids.add(referral.pathway_id)

            mandatory_filter_form_ids = {
                mandatory_forms[fid]
                for pid in pathway_ids
                for fid in pf_map.get(pid, set())
                if fid in mandatory_forms
            }

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

        logger.info(f"Calculated adherence for {len(results)} episodes")
        return pd.DataFrame(results)

    def days_to_treatment(self):
        """
        Calculates days between episode start and treatment start based on first relevant form submission.

        Returns:
            pd.DataFrame: DataFrame with subject ID, episode ID, episode start date,
                          treatment start date, and days to treatment.
        """
        logger.info("Calculating days to treatment")
        episodes = self.db.query(Episode).filter(Episode.start_date.isnot(None)).all()
        af_forms = self.db.query(AfFormData).all()

        min_index_map = self._get_min_index_map()
        summary_map = self._get_summary_map()
        aff_instance_map = self._get_aff_instance_map(af_forms)
        referral_map = self._get_referral_map()

        records = []
        for ep in episodes:
            episode_id = ep.episode_id
            subject_id = ep.subject_id
            episode_start = ep.start_date

            # Aggregate pathway IDs from episode and referrals
            pathway_ids = {ep.pathway_id} if ep.pathway_id else set()
            pathway_ids.update(
                rd.pathway_id for rd in referral_map.get(episode_id, []) if rd.pathway_id
            )

            # Get form IDs relevant to treatment start
            form_ids = [
                summary_map[min_index_map[pid][0]]
                for pid in pathway_ids
                if pid in min_index_map and min_index_map[pid][0] in summary_map
            ]

            aff_instances = aff_instance_map.get(episode_id, {})
            treatment_dates = [aff_instances[fid] for fid in form_ids if fid in aff_instances]

            if not treatment_dates:
                continue

            treatment_start = min(treatment_dates)
            days_to_treatment = (episode_start - treatment_start).days
            records.append({
                "subject_id": subject_id,
                "episode_id": episode_id,
                "episode_start": episode_start,
                "treatment_start_date": treatment_start,
                "days_to_treatment_start": days_to_treatment
            })

        logger.info(f"Calculated days to treatment for {len(records)} episodes")
        return pd.DataFrame(records)
