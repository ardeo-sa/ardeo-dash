# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.metrics import Base

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    # Mock DB URI
    monkeypatch.setenv("PRIMARY_DB_URI", "sqlite:///./primary.db")
    monkeypatch.setenv("METRICS_DB_URI", "sqlite:///./metrics.db")
    import importlib
    import app.config
    importlib.reload(app.config)

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
