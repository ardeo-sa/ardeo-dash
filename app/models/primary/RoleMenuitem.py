from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class RoleMenuitem(Base):
    __tablename__ = 'role_menuitem'

    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True, nullable=False)
    menuitem_id = Column(Integer, ForeignKey('menu_item.id'), primary_key=True, nullable=False)
    roles = relationship('Roles')
    menu_item = relationship('Menu_item')
