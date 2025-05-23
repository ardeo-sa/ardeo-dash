from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database.metrics import Base


class Organisation(Base):

    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, nullable=False)