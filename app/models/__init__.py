"""
Database session initialization.

Initialize SQLAlchemy session for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///models/enterprise.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Get session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
