from sqlalchemy import Column, Integer, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class RoleMenuitem(Base):
    __tablename__ = 'role_menuitem'

    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True, nullable=False)
    menuitem_id = Column(Integer, ForeignKey('menu_item.id'), primary_key=True, nullable=False)
    roles = relationship('Roles')
    menu_item = relationship('Menu_item')
