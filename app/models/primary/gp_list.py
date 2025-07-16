"""
Represents a list of general practitioners (GPs),
capturing essential details about their practice locations, contact information,
and affiliations. This model is designed to facilitate the integration and management
of GP details from external data sources.
"""

from sqlalchemy import Column, String

from app.config import Base

class GpList(Base):
    """
    Represents a list of general practitioners (GPs),
    capturing essential details about their practice locations, contact information,
     and affiliations. This model is designed to facilitate the integration and management
     of GP details from external data sources.
    Attributes:
    GPNo : str Unique identifier for the GP, serving as the primary key.
    Health_Centre_or_Road : str Address line for the health centre or road where the GP is located.
    Town_or_City : str Town or city of the GP's practice.
    County : str County or region of the GP's practice.
    gpAddress4 : str Additional address line for the GP's practice.
    gpEmailAddress : str  Email address for contacting the GP.
    gpFaxNumber : str  Fax number for the GP's practice.
    Initial : str Initials of the GP.
    gpPctCode : str  Code for the Primary Care Trust (PCT) the GP is associated with.
    gpPctName : str  Name of the Primary Care Trust (PCT).
    gpPostcode : str  Postal code for the GP's practice.
    gpPracticeCode : str Code for the GP's practice.
    gpPracticeName : str Name of the GP's practice.
    Name : str  Full name of the GP.
    Phone : str  Phone number for contacting the GP.
    """
    __tablename__ = 'gp_list'

    GPNo = Column(String, primary_key=True, nullable=False)
    Health_Centre_or_Road = Column(String)
    Town_or_City = Column(String)
    County = Column(String)
    gpAddress4 = Column(String)
    gpEmailAddress = Column(String)
    gpFaxNumber = Column(String)
    Initial = Column(String)
    gpPctCode = Column(String)
    gpPctName = Column(String)
    gpPostcode = Column(String)
    gpPracticeCode = Column(String)
    gpPracticeName = Column(String)
    Name = Column(String)
    Phone = Column(String)
