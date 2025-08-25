"""
Manages system-wide configurable options as key-value pairs, enabling flexible
and dynamic adjustment of messaging and application settings without code changes.
"""

from sqlalchemy import Column, Integer, String
from app.config import Base


class SystemOptionKeyvalue(Base):
    """
    Manages system-wide options and settings, providing a flexible mechanism for configuring
    messaging aspects of the application.
     This model allows for the management of key-value pairs representing system options,
     enabling dynamic configuration adjustments without modifying code.

    Attributes:
    id : intUnique identifier for the system option.
    isActive : str Indicates whether the option is currently active ("Yes" or "No").
    description : str Description of the system option and its purpose.
    isEnabled : strIndicates whether the option is enabled ("Yes" or "No").
    FlagLevel : strLevel or category of the flag (e.g., "System", "User").
    system_key : strUnique key identifying the system option.
    """
    __tablename__ = 'system_option_keyvalue'

    id = Column(Integer, primary_key=True, nullable=False)
    isActive = Column(String, nullable=False)
    description = Column(String)
    isEnabled = Column(String, nullable=False)
    FlagLevel = Column(String)
    system_key = Column(String, nullable=False)
