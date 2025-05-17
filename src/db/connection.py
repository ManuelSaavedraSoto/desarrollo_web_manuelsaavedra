"""DB connection for the application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()


# Create all tables
def db_init():
    """Initialize the database and create all tables."""
    # Import models here to avoid circular imports
    from . import (
        models,
    )  # pylint: disable=import-outside-toplevel disable=unused-import

    # Create all tables in the database
    Base.metadata.create_all(engine)
