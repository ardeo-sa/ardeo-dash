"""
This package module imports core primary models and association tables used throughout the application.

It provides convenient access to key database models related to users, roles, organisations, identifiers,
summary records, pathways, and patient care, centralizing imports for easier usage.

Imported models and tables include:

- IdentifierContext, Identifiers: Models managing identification contexts and identifiers.
- Organisation: Model representing organisational entities.
- Roles, user_roles, Users: User management and role association models.
- Summary: Model for summary records.
- Pathway-related models and mappings: Pathway, PathwayForms, PathwayFormSummaryMap, PathwayGroups,
  and various mapping/order tables for pathway form summaries and groups.
- PatientCareProviders, Episode, Subject: Models related to patient care and clinical episodes.

Including these imports here allows other parts of the application to import primary models directly
from this package, improving code organization and import clarity.
"""

from app.models.primary.identifier_context import IdentifierContext
from app.models.primary.identifiers import Identifiers
from app.models.primary.organisation import Organisation
from app.models.primary.roles import Roles
from app.models.primary.users import user_roles
from app.models.primary.users import Users
from app.models.primary.summary import Summary

from app.models.primary.pathway import Pathway
from app.models.primary.pathway_forms import PathwayForms
from app.models.primary.pathway import pathway_form_map
from app.models.primary.pathway import pathway_groups_map
from app.models.primary.pathway import group_map_order
from app.models.primary.pathway import pathway_summaries
from app.models.primary.pathway import pathway_formsummary_map_order
from app.models.primary.pathway_form_summary_map import PathwayFormSummaryMap
from app.models.primary.pathway_groups import PathwayGroups
from app.models.primary.pathway_groups_map_order import PathwayGroupsMapOrder

from app.models.primary.patient_care_providers import PatientCareProviders
from app.models.primary.episode import Episode
from app.models.primary.subject import Subject
