from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config import Base
from sqlalchemy.orm import relationship

from app.models.primary import Pathway


class Episode(Base):
    __tablename__ = 'episode'

    episode_id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    speciality = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    status = Column(String)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)

    item_index = Column(Integer)

    assistant_id = Column(Integer, ForeignKey('users.user_id'))
    assistant = relationship('Users', foreign_keys=[assistant_id])

    primary_specialist_id = Column(Integer, ForeignKey('users.user_id'))
    primary_specialist = relationship('Users', foreign_keys=[primary_specialist_id])

    subject = relationship('Subject',foreign_keys=[subject_id])
    pathway_id = Column(Integer, ForeignKey('pathway.id'))
    pathway = relationship(Pathway)