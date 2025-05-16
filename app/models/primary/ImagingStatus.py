from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ImagingStatus(Base):
    __tablename__ = 'imaging_status'

    imaging_status_id = Column(Integer, primary_key=True, nullable=False)
    accession_number = Column(String, nullable=False)
    episode_id = Column(Integer, nullable=False)
    current_status = Column(Integer, nullable=False)
    last_modified_date = Column(DateTime, nullable=False)
    note_id = Column(Integer, nullable=False)
    is_notified = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisation.id'))
    image_transfer_method_id = Column(Integer, ForeignKey('image_transfer_method.id'))
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    organisation = relationship('Organisation')
    image_transfer_method = relationship('Image_transfer_method')
    subject = relationship('Subject')
