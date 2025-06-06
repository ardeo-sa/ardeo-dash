from sqlalchemy import Column, Integer, String
from app.config import Base

class Settings(Base):
    """
    Represents system-wide settings, providing a structured way to manage and persist
    application configuration parameters. This model replaces a traditional properties file,
    offering better organization, version control, and data management capabilities.

    Attributes:
    id : int Unique identifier for the setting.
    description : str Description of the setting and its purpose.
    Property_key : strUnique key identifying the setting.
    Property_value : strValue of the setting.
    """
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String)
    Property_key = Column(String, nullable=False)
    Property_value = Column(String)
