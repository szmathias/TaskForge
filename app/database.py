"""
Database configuration and session management.

This module sets up the SQLAlchemy engine, session factory, and base class
for database models. It also provides a dependency function for database sessions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session.

    Yields:
        Session: SQLAlchemy database session

    Note:
        Automatically closes the session after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
