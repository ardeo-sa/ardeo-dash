from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Episode(Base):
    __tablename__ = 'episode'

    episode_id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    speciality = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    status = Column(String)

    assistant_id = Column(Integer, ForeignKey('assistant.user_id'))
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    primary_specialist_id = Column(Integer, ForeignKey('primary_specialist.user_id'))

    pathway_id = Column(Integer, ForeignKey('pathway.pathway_id'))
    item_index = Column(Integer)

    assistant = relationship("Users", foreign_keys=[assistant_id])
    primary_specialist = relationship("Users", foreign_keys=[primary_specialist_id])
    subject = relationship('Subject')
    pathway = relationship('Pathway')

