from sqlalchemy import Column, Integer, String
from app.config import Base

class Acl(Base):
    """
       ORM model representing an Access Control List (ACL).

       An ACL governs access to a resource identified by its unique name.
       Each ACL has an owner and can contain multiple entries granting
       permissions to users or groups.

       Attributes:
           acl_id (int): Primary key identifier for the ACL.
           acl_name (str): Unique name identifying the ACL resource.
           acl_ownername (str): Name of the user who owns this ACL.
       """
    __tablename__ = 'acl'

    acl_id = Column(Integer, primary_key=True, nullable=False)
    acl_name = Column(String, nullable=False)
    acl_ownername = Column(String, nullable=False)
