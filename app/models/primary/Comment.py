from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comment'

    comments_id = Column(Integer, primary_key=True, nullable=False)
    attached_file = Column(String)
    comment = Column(String)
    dateOfComment = Column(DateTime)
    formPageIndex = Column(Integer)
    guid = Column(String, nullable=False)
    isDeleted = Column(String, nullable=False)
    pageName = Column(String)
    document_metadata_id = Column(Integer, ForeignKey('patient_documents.id'))
    commenting_user_id = Column(Integer, ForeignKey('users.user_id'))
    meeting_item_id = Column(Integer, ForeignKey('meeting_item.meetingitem_id'))
    consultationNoteId = Column(Integer, ForeignKey('af_form_data.af_id'))
    patientId = Column(Integer, ForeignKey('patient.patient_id'))
    patient_documents = relationship('Patient_documents')
    users = relationship('Users')
    meeting_item = relationship('Meeting_item')
    af_form_data = relationship('Af_form_data')
    patient = relationship('Patient')
