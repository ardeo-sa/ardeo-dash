"""
Represents a menu item within the system, used for configuring system and report menus
based on user roles. This model supports dynamic menu management, allowing for personalized user experiences.
"""

from sqlalchemy import Column, Integer, String
from app.config import Base


class MenuItem(Base):
    """
    Represents a menu item within the system, used for configuring system and report menus
    based on user roles.  This model supports dynamic menu management, allowing for personalized user experiences.
    Attributes:
    id : int Unique identifier for the menu item.
    category : str  Category to which the menu item belongs (e.g., reports, settings).
    description : str Detailed description of the menu item.
    name : str  Name of the menu item, displayed to users.
    published : str Flag indicating whether the menu item is published ("Yes" or "No").
    """
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String)
    description = Column(String)
    name = Column(String, nullable=False)
    published = Column(String)
