"""
Represents a Picture Archiving and Communication System (PACS) for
managing and transferring medical images within an external system.
This model facilitates the configuration and integration of PACS for streamlined image handling.

Attributes:
----------
id : int
    Unique identifier for the PACS configuration.
aet : str
    Application Entity Title (AET) for the PACS, identifying the system in DICOM communications.
description : str
    Description of the PACS system, detailing its purpose or configuration.
enabled : str
    Flag indicating whether the PACS is enabled ("Yes" or "No").
ip : str
    IP address for the PACS, used for network communications.
name : str
    Name of the PACS system.
port : str
    Network port used for PACS communications.
"""

from sqlalchemy import Column, Integer, String

from app.config import Base


class Pacs(Base):
    """
    Represents a Picture Archiving and Communication System (PACS) for
     managing and transferring medical images within an external system.
     This model facilitates the configuration and integration of PACS for streamlined image handling.
    Attributes:
    id : int  Unique identifier for the PACS configuration.
    aet : str   Application Entity Title (AET) for the PACS, identifying the system in DICOM communications.
    description : str  Description of the PACS system, detailing its purpose or configuration.
    enabled : str  Flag indicating whether the PACS is enabled ("Yes" or "No").
    ip : str  IP address for the PACS, used for network communications.
    name : str  Name of the PACS system.
    port : str Network port used for PACS communications.
    """
    __tablename__ = 'pacs'

    id = Column(Integer, primary_key=True, nullable=False)
    aet = Column(String)
    description = Column(String)
    enabled = Column(String)
    ip = Column(String)
    name = Column(String)
    port = Column(String)
