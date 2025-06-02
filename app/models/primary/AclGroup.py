from sqlalchemy.orm import relationship

from app.config import Base


class AclGroup(Base):
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }

    members = relationship("GroupUsername", back_populates="group", cascade="all, delete-orphan")