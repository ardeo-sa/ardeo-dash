"""
Represents an organisation within the system, capturing essential details such as its address,
operational status, and integration with identifier contexts.
This model supports the management of organisations as entities in a larger network,
facilitating coordination and data sharing.

Attributes:
----------
id : int
    Unique identifier for the organisation.
address : str
    Physical address of the organisation.
is_central_hub : str
    Flag indicating if the organisation serves as a central hub ("Yes" or "No").
city : str
    City where the organisation is located.
creation_date : datetime
    Date when the organisation was added to the system.
code : str
    Unique code assigned to the organisation for identification.
description : str
    Brief description of the organisation.
name : str
    Name of the organisation.
modified_date : datetime
    Date when the organisation's details were last modified.
postcode : str
    Postal code for the organisation's location.
hosts_virtual_mdm : str
    Flag indicating if the organisation hosts a virtual Master Data Management (MDM) system ("Yes" or "No").
context_id : int
    Foreign key linking to the IdentifierContext, indicating the namespace for patient identifiers.

Relationships:
-------------
identifier_context : IdentifierContext
    Relationship with the IdentifierContext model, providing access to the context details.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class Organisation(Base):
    """
    Represents an organisation within the system, capturing essential details such as its address,
    operational status, and integration with identifier contexts.
    This model supports the management of organisations as entities in a larger network,
    facilitating coordination and data sharing.
    Attributes:
    id : int Unique identifier for the organisation.
    address : str Physical address of the organisation.
    is_central_hub : str Flag indicating if the organisation serves as a central hub ("Yes" or "No").
    city : str City where the organisation is located.
    creation_date : datetime  Date when the organisation was added to the system.
    code : str  Unique code assigned to the organisation for identification.
    description : str  Brief description of the organisation.
    name : str  Name of the organisation.
    modified_date : datetime Date when the organisation's details were last modified.
    postcode : str Postal code for the organisation's location.
    hosts_virtual_mdm : str Flag indicating if the organisation hosts a virtual Master Data Management (MDM) system ("Yes" or "No").
    context_id : intForeign key linking to the IdentifierContext, indicating the namespace for patient identifiers.
    Relationships:
    identifier_context : Relationship with the IdentifierContext model, providing access to the context details.
    """
    __tablename__ = 'organisation'
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String)
    is_central_hub = Column(String)
    city = Column(String)
    creation_date = Column(DateTime, nullable=False)
    code = Column(String, nullable=False)
    description = Column(String)
    name = Column(String)
    modified_date = Column(DateTime, nullable=False)
    postcode = Column(String)
    hosts_virtual_mdm = Column(String)
    context_id = Column(Integer, ForeignKey('identifier_context.context_id'))
    identifier_context = relationship('IdentifierContext')
