from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MeetingItemImages(Base):
    __tablename__ = 'meeting_item_images'

    id = Column(Integer, primary_key=True, nullable=False)
    file_id = Column(Integer)
    filename = Column(String)
    instance_uid = Column(String)
    notes = Column(String)
    patientDocumentMetaDataId = Column(Integer)
    seriesDateAndTime = Column(String)
    seriesDescription = Column(String)
    series_uid = Column(String)
    seriesModality = Column(String)
    study_uid = Column(String)
    meetingItem_id = Column(Integer, ForeignKey('meeting_item.meetingitem_id'), nullable=False)
    meeting_item = relationship('Meeting_item')
