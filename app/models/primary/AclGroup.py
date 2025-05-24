from sqlalchemy.orm import relationship

from app.models.primary import AclPrincipal


class AclGroup(Principal):
    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }

    members = relationship("GroupUsername", back_populates="group", cascade="all, delete-orphan")