from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class PathwayGroupsMapOrder(Base):
    """
    Manages the ordering of groups within clinical pathways, ensuring that group sequences
    are maintained for effective execution of pathway protocols.
    This model supports the organization of pathway components by defining precise group orderings.

    Attributes:
    pathway_id : int Foreign key linking to the Pathway model, indicating the associated pathway.
    pathway_group_id : int Foreign key linking to the PathwayGroups model, representing the group within the pathway.
    groupMapOrder_KEY : int Key defining the order of groups within the pathway, ensuring clear sequencing.

    Relationships:
    pathway : Relationship with the Pathway model to access pathway details and maintain order integrity.
    """
    __tablename__ = 'pathway_groups_map_order'
    __table_args__ = {'extend_existing': True}
    pathway_id = Column(Integer, ForeignKey('pathway.id'), primary_key=True, nullable=False)
    pathway_group_id = Column(Integer , ForeignKey('pathway_groups.pathway_group_id'), primary_key=True, )
    groupMapOrder_KEY = Column(Integer, primary_key=True, nullable=False)
    pathway = relationship('Pathway')
