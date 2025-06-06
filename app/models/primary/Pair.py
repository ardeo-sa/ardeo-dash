from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class Pair(Base):
    """
    Represents a pair of related values within a named list, facilitating the management
    of key-value relationships in structured data sets. This model is useful for
    scenarios where pairs of data need to be managed and accessed efficiently.

    Attributes:
    pair_id : int Unique identifier for the pair.
    nl_filter_org_code : strOptional filter code to associate the pair with a specific organisation.
    pair_first : str The first element of the pair, typically used as a key.
    pair_second : strThe second element of the pair, typically used as a value.
    namedList_id : int Foreign key linking to the NamedList model, indicating the list to which the pair belongs.
    child_index : int Index used for ordering pairs within the named list.

    Relationships:
    named_list : Relationship with the NamedList model to access list details and maintain pair associations.
    """
    __tablename__ = 'pair'

    pair_id = Column(Integer, primary_key=True, nullable=False)
    nl_filter_org_code = Column(String)
    pair_first = Column(String, nullable=False)
    pair_second = Column(String, nullable=False)
    namedList_id = Column(Integer, ForeignKey('named_list.nl_id'))
    child_index = Column(Integer)
    named_list = relationship('Named_list')
