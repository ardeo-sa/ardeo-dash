from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship

class RoleMenuitem(Base):
    """
     Defines the relationship between roles and menu items, controlling access to
     menu items based on user roles.  This model is crucial for implementing
      role-based access control (RBAC) in the system, ensuring that only authorized
       users can access specific functionalities.

    Attributes:
    role_id : int   Foreign key referencing the `roles` table, specifying the role.
    menuitem_id : int   Foreign key referencing the `menu_item` table, specifying the menu item.

    Relationships:
    roles :  Relationship to the `Roles` model for accessing role details.
    menu_item : Relationship to the `Menu_item` model for accessing menu item details.
     """
    __tablename__ = 'role_menuitem'

    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True, nullable=False)
    menuitem_id = Column(Integer, ForeignKey('menu_item.id'), primary_key=True, nullable=False)
    roles = relationship('Roles')
    menu_item = relationship('Menu_item')
