"""
Database models for URL Detect.

SQLAlchemy ORM models for:
- Tenant (multi-tenant support)
- RequestLog (audit logging)
- PhishTankCache (threat intel caching)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Create engine
from sqlalchemy import create_engine
DATABASE_URL = "sqlite:///models/enterprise.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


class Tenant(Base):
    """Tenant entity for multi-tenant API support."""
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    api_key = Column(String(64), nullable=False, unique=True)  # SHA256 hash
    tier = Column(String(20), default="free")  # free, pro, enterprise
    quota_daily = Column(Integer, default=100)  # Daily request limit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Index for API key lookup
    __table_args__ = (
        Index("idx_tenants_api_key", "api_key"),
    )
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', tier='{self.tier}')>"


class RequestLog(Base):
    """Audit log for API requests."""
    __tablename__ = "request_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url_hash = Column(String(64), nullable=False)  # SHA256 hash of URL
    prediction = Column(String(20), nullable=False)  # phishing/legitimate
    risk_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Index for analytics queries
    __table_args__ = (
        Index("idx_request_logs_created", "created_at"),
        Index("idx_request_logs_url_hash", "url_hash"),
    )
    
    def __repr__(self):
        return f"<RequestLog(id={self.id}, url_hash='{self.url_hash[:16]}...', prediction='{self.prediction}')>"


class PhishTankCache(Base):
    """Cache for PhishTank API responses."""
    __tablename__ = "phish_tank_cache"
    
    url_hash = Column(String(64), primary_key=True, nullable=False)
    result = Column(String, nullable=False)  # JSON string
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Index for cache lookup
    __table_args__ = (
        Index("idx_phish_tank_cache_expires", "expires_at"),
    )
    
    def __repr__(self):
        return f"<PhishTankCache(url_hash='{self.url_hash[:16]}...', expires_at='{self.expires_at}')>"
