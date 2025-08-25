"""
Represents a patient within the healthcare system, storing demographic, contact, and medical data.

Relationships:
- users: creator of the record.
- provider_details: healthcare providers linked to the subject over time.
- episodes: clinical episodes associated with the subject.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base

class Subject(Base):
    """
    Represents a subject (patient) within the healthcare system, encompassing a wide range of
    demographic, contact, and medical information. This model serves as a central repository
     for patient-related data, facilitating efficient management and coordination of care.

    Attributes:
    subject_id : int   Unique identifier for the subject.
    address : str   Subject's address.
    patient_admitting_physician : int Identifier for the admitting physician.
    allergies : str  Subject's allergies.
    assessment_plan : str  Assessment and care plan for the subject.
    country : str Subject's country of residence.
    creating_user_id : int    Identifier for the user who created the record.
    created_date : datetime  Date and time when the record was created.
    birth_date : datetime Subject's date of birth.
    death_date : datetime   Subject's date of death (if applicable).
    death_indicator : str Indicates if the subject is deceased ("Yes" or "No").
    email : str Subject's email address.
    ethnicity : str Subject's ethnicity.
    forename : str  Subject's first name.
    fullname : str  Subject's full name.
    gp_email : str  Email address of the subject's general practitioner (GP).
    gp_fax : str  Fax number of the subject's GP.
    gp_forename : str First name of the subject's GP.
    gp_gmp_code : str  GMP code of the subject's GP.
    gp_pct_code : str PCT code of the subject's GP.
    gp_pct_name : str Name of the PCT associated with the subject's GP.
    gp_postcode : str  Postal code of the subject's GP.
    gp_practice_code : str   Practice code of the subject's GP.
    gp_practice_name : str Name of the subject's GP's practice.
    gp_address : str Address of the subject's GP.
    gp_surname : str  Surname of the subject's GP.
    gp_phone : str  Phone number of the subject's GP.
    guid : str Globally unique identifier for the subject.
    home_phone : str Subject's home phone number.
    image_url : str URL for the subject's image (if applicable).
    language : str  Subject's preferred language.
    marital_status : str Subject's marital status.
    middle_name : str  Subject's middle name.
    mobile_phone : str Subject's mobile phone number.
    modified_date : datetime  Date and time when the record was last modified.
    nationality : str Subject's nationality.
    nhs_number : str   Subject's NHS number.
    nok_address : str   Address of the next of kin (NOK).
    nok_country : str Country of the NOK.
    nok_frename : str First name of the NOK.
    nok_postcode : str  Postal code of the NOK.
    nok_relationship : str  Relationship of the NOK to the subject.
    nok_surname : str Surname of the NOK.
    nok_phone_1 : str First phone number of the NOK.
    nok_phone_2 : str  Second phone number of the NOK.
    occupation : str  Subject's occupation.
    overseas_visitor : str Indicates if the subject is an overseas visitor ("Yes" or "No").
    postcode : str Subject's postal code.
    priority : int  Priority level assigned to the subject.
    is_disabled : str   Indicates if the subject is disabled ("Yes" or "No").
    religion : str  Subject's religion.
    sex : str Subject's sex.
    surname : str Subject's surname.
    title : str  Subject's title (e.g., Mr., Mrs.).
    work_phone : str Subject's work phone number.
    user_user_id : int  Foreign key linking to the Users model, representing the user associated with the subject.

    Relationships:
    users : a one-to-many relationship with Users. the user who created the record,
    provider_details: relationship Represents the details of healthcare providers associated with this subject.
    A subject can have multiple providers over time.
    episodes : A one-to-many relationship with Episode. Represents the clinical episodes associated with this subject.
    A subject can be involved in multiple episodes of care.
    """
    __tablename__ = 'subject'
    subject_id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String)
    patient_admitting_physician = Column(Integer)
    allergies = Column(String)
    assessment_plan = Column(String)
    country = Column(String)
    creating_user_id = Column(Integer)
    created_date = Column(DateTime)
    birth_date = Column(DateTime)
    death_date = Column(DateTime)
    death_indicator = Column(String)
    email = Column(String)
    ethnicity = Column(String)
    forename = Column(String)
    fullname = Column(String)
    gp_email = Column(String)
    gp_fax = Column(String)
    gp_forename = Column(String)
    gp_gmp_code = Column(String)
    gp_pct_code = Column(String)
    gp_pct_name = Column(String)
    gp_postcode = Column(String)
    gp_practice_code = Column(String)
    gp_practice_name = Column(String)
    gp_address = Column(String)
    gp_surname = Column(String)
    gp_phone = Column(String)
    guid = Column(String, nullable=False)
    home_phone = Column(String)
    image_url = Column(String)
    language = Column(String)
    marital_status = Column(String)
    middle_name = Column(String)
    mobile_phone = Column(String)
    modified_date = Column(DateTime)
    nationality = Column(String)
    nhs_number = Column(String)
    nok_address = Column(String)
    nok_country = Column(String)
    nok_frename = Column(String)
    nok_postcode = Column(String)
    nok_relationship = Column(String)
    nok_surname = Column(String)
    nok_phone_1 = Column(String)
    nok_phone_2 = Column(String)
    occupation = Column(String)
    overseas_visitor = Column(String)
    postcode = Column(String)
    priority = Column(Integer, nullable=False)
    is_disabled = Column(String)
    religion = Column(String)
    sex = Column(String)
    surname = Column(String)
    title = Column(String)
    work_phone = Column(String)
    user_user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
