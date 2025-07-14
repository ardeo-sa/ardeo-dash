from sqlalchemy import Column, Integer
from app.config import Base



class UserSpeciality(Base):
    """
    Represents the association between users and their medical specialities,
    enabling the management and tracking of user expertise within the healthcare system.
    This model is crucial for assigning users to tasks or projects based on their area
    of specialization.

    Attributes:

    id : intUnique identifier for the user-speciality association.
    speciality_id : int Foreign key referencing the `speciality` table, indicating the speciality.
    user_id : int Foreign key referencing the `users` table, indicating the user.
    """
    __tablename__ = 'user_speciality'

    id = Column(Integer, primary_key=True, nullable=False)
    speciality_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
