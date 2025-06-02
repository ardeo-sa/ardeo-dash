from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship



class JwtTokens(Base):
    __tablename__ = 'jwt_tokens'

    id = Column(Integer, primary_key=True, nullable=False)
    expired = Column(String, nullable=False)
    revoked = Column(String, nullable=False)
    token = Column(String)
    tokenType = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    users = relationship('Users')
