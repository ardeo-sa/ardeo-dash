from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CancerBiopsyReportVw(Base):
    __tablename__ = 'cancer_biopsy_report_vw'

    lab_order_number = Column(String, primary_key=True, nullable=False)
    Biopsy_Date = Column(DateTime)
    Date_Received = Column(DateTime)
    GP_Cons = Column(String)
    Hospital = Column(String)
    Lab_Name = Column(String)
    Lab_Tel_Nbr = Column(String)
    ltr_id = Column(String)
    ltr_name = Column(String)
    Report_txt_clean = Column(String)
    ltr_result_status = Column(String)
    ltr_set_id = Column(Integer)
    Pat_Address1 = Column(String)
    Pat_DOB = Column(DateTime)
    Pat_Forename = Column(String)
    Pat_gender = Column(String)
    Pat_Postcode = Column(String)
    Pat_Surname = Column(String)
    Report_Created_Dt = Column(DateTime)
    Report_Edit_Dt = Column(DateTime)
    SAP_MPI = Column(String)
    Source = Column(String)
    test_service_id = Column(String)
    test_specimen_name = Column(String)
