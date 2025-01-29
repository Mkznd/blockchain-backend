import pytest
from sqlmodel import SQLModel, create_engine, Session

from settings import settings

# Use the same database URL as in settings
DATABASE_URL = settings.database_url

# Create an SQLite engine
engine = create_engine(DATABASE_URL, echo=True)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure tables are created before running tests."""
    SQLModel.metadata.create_all(engine)  # This will create tables

    yield  # Run tests

    # Optional: Cleanup after tests (uncomment if needed)
    # SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session():
    """Provides a transactional database session for each test."""
    with Session(engine) as session:
        yield session  # Pass session to tests
