from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PatientDocuments(Base):
    __tablename__ = 'patient_documents'

    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String)
    commentsGuid = Column(String)
    fileName = Column(String)
    guid = Column(String, nullable=False)
    noteGuid = Column(String)
    original_name = Column(String)
    patientGuid = Column(String)
    title = Column(String)
    uploadedOn = Column(DateTime)
    uploadedBy = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
