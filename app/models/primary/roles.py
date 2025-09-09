"""
Defines the Roles model to manage user roles and permissions within the system.
"""

from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship

from app.config import Base

# Define the association table FIRST
class Roles(Base):
    """
        Defines user roles within the system, specifying permissions and access levels.
        This model is essential for implementing Role-Based Access Control ,
        ensuring that users only have access to functionalities relevant to their assigned roles.
        Attributes:
             role_id : int Unique identifier for the role.
             description : str Description of the role and its associated permissions.
             is_desktop : str Flag indicating whether the role is for desktop access ("Yes" or "No").
             enabled : strFlag indicating whether the role is currently active ("Yes" or "No").
             value : strUnique value representing the role (often used for referencing in other parts of the system).
    """
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String)
    is_desktop = Column(String)
    enabled = Column(String, nullable=False)
    value = Column(String, nullable=False)
