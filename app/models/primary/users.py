"""
Represents system users, managing their authentication, profile details, and role assignments.
Central to user management and access control with many-to-many roles and organizational association.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from app.config import Base

# Now that 'roles' table is defined, define the association table
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.role_id'), nullable=False)
)

class Users(Base):
    """
    Represents users within the system, storing user details, authentication information,
    and role assignments.  This model is central to managing user accounts and access control.

    Attributes:
    user_id : int  Unique identifier for the user.
    accountNonExpired : str  Flag indicating if the account is not expired ("Yes" or "No").
    accountNonLocked : str  Flag indicating if the account is not locked ("Yes" or "No").
    user_can_edit : str  Flag indicating if the user can edit their profile ("Yes" or "No").
    creation_date : datetime  Date and time when the user account was created.
    credentialsNonExpired : str    Flag indicating if user credentials are not expired ("Yes" or "No").
    dateAccountExpires : datetime Date when the user account expires (if applicable).
    datePasswordLastChanged : datetime  Date when the user's password was last changed.
    deleted : str  Flag indicating if the user account is deleted ("Yes" or "No").
    email : str  User's email address.
    email_verified : str   Flag indicating if the user's email address is verified ("Yes" or "No").
    enabled : str  Flag indicating if the user account is enabled ("Yes" or "No").
    enforceStrongPassword : str  Flag indicating if strong password enforcement is enabled for the user ("Yes" or "No").
    external_ldap_user_id : str Identifier for the user in an external LDAP system (if applicable).
    user_forename : str  User's first name.
    google_user : str  Flag indicating if the user is authenticated via Google ("Yes" or "No").
    guid : str Globally unique identifier for the user.
    is_subject : str Flag indicating if the user is also a subject (patient) ("Yes" or "No").
    ldap_user : str   Flag indicating if the user is managed via LDAP ("Yes" or "No").
    user_middlename : str  User's middle name.
    modified_date : datetime  Date and time when the user record was last modified.
    user_nickname : str  User's nickname.
    password : str  User's password (stored securely!).
    passwordCanExpire : str Flag indicating if the user's password can expire ("Yes" or "No").
    user_prefix : str User's prefix (e.g., "Dr.").
    profileImagePath : str   Path to the user's profile image.
    secret : str  Secret value (e.g., for 2FA).
    user_suffix : str  User's suffix (e.g., "Jr.").
    user_surname : str  User's surname.
    username : str  User's username.
    using2FA : str  Flag indicating if the user is using 2FA ("Yes" or "No").
    organisation_id : int Foreign key linking to the Organisation model.

    Relationships:
    roles :  Many-to-many relationship with Roles, defining the user's roles.  Uses the `user_roles` association table.
    organisation : Relationship with the Organisation model.

    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    accountNonExpired = Column(String, nullable=False)
    accountNonLocked = Column(String, nullable=False)
    user_can_edit = Column(String)
    creation_date = Column(DateTime)
    credentialsNonExpired = Column(String, nullable=False)
    dateAccountExpires = Column(DateTime)
    datePasswordLastChanged = Column(DateTime)
    deleted = Column(String)
    email = Column(String)
    email_verified = Column(String, nullable=False)
    enabled = Column(String, nullable=False)
    enforceStrongPassword = Column(String, nullable=False)
    external_ldap_user_id = Column(String)
    user_forename = Column(String)
    google_user = Column(String, nullable=False)
    guid = Column(String, nullable=False)
    is_subject = Column(String, nullable=False)
    ldap_user = Column(String, nullable=False)
    user_middlename = Column(String)
    modified_date = Column(DateTime)
    user_nickname = Column(String)
    password = Column(String, nullable=False)
    passwordCanExpire = Column(String)
    user_prefix = Column(String)
    profileImagePath = Column(String)
    secret = Column(String, nullable=False)
    user_suffix = Column(String)
    user_surname = Column(String)
    username = Column(String, nullable=False)
    using2FA = Column(String, nullable=False)
    roles = relationship("Roles", secondary=user_roles, backref="users", lazy="joined")
    organisation_id = Column(Integer, ForeignKey('organisation.id'))
    organisation = relationship('Organisation')
