"""
Represents groups within clinical pathways, organizing them into logical units
for effective management and execution of care processes.
This model helps in categorizing pathway components and ensuring that all necessary
groupings are well-defined and maintained.

Attributes:
-----------
pathway_group_id : int
    Unique identifier for the pathway group.
group_name : str
    Name of the group, providing a clear label for identification and reference.
is_system : str
    Flag indicating whether the group is a system-defined group ("Yes" or "No").
"""

from sqlalchemy import Column, Integer, String

from app.config import Base

class PathwayGroups(Base):
    """
     Represents groups within clinical pathways, organizing them into logical units
     for effective management and execution of care processes.
     This model helps in categorizing pathway components and ensuring that all necessary
     groupings are well-defined and maintained.

    Attributes:
    pathway_group_id : int Unique identifier for the pathway group.
    group_name : str   Name of the group, providing a clear label for identification and reference.
    is_system : str  Flag indicating whether the group is a system-defined group ("Yes" or "No").
    """
    __tablename__ = 'pathway_groups'
    pathway_group_id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String, nullable=False)
    is_system = Column(String, nullable=False)
