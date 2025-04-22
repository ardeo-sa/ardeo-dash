
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import PRIMARY_DB_URI

primary_engine = create_engine(PRIMARY_DB_URI)
PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)
