"""
Multi-Tenant API Routes.

Endpoints:
- GET /v1/tenant/{id}: Get tenant info (admin)
- POST /v1/tenant: Create tenant (admin)
- DELETE /v1/tenant/{id}: Delete tenant (admin)
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.database import Tenant, RequestLog
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    """Get database session dependency."""
    from app.models.database import db_session
    if db_session is None:
        raise RuntimeError("Database session not initialized")
    return db_session()

class TenantCreate(BaseModel):
    name: str
    tier: Optional[str] = "free"
    quota_daily: Optional[int] = 100

class TenantResponse(BaseModel):
    id: int
    name: str
    tier: str
    quota_daily: int
    created_at: str

@router.get("/v1/tenant/{tenant_id}")
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """
    Get tenant information.
    
    Args:
        tenant_id: Tenant ID
        db: Database session
        
    Returns:
        Tenant details
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        tier=tenant.tier,
        quota_daily=tenant.quota_daily,
        created_at=tenant.created_at.isoformat() if tenant.created_at else None
    )

@router.post("/v1/tenant")
def create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new tenant.
    
    Args:
        payload: TenantCreate with name, tier, quota_daily
        db: Database session
        
    Returns:
        Created tenant details
    """
    # Check if tenant already exists
    existing = db.query(Tenant).filter(Tenant.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tenant already exists")
    
    # Create new tenant
    from datetime import datetime
    tenant = Tenant(
        name=payload.name,
        api_key=f"tk_{payload.name.lower()}",  # Placeholder API key
        tier=payload.tier,
        quota_daily=payload.quota_daily,
        created_at=datetime.utcnow()
    )
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        tier=tenant.tier,
        quota_daily=tenant.quota_daily,
        created_at=tenant.created_at.isoformat() if tenant.created_at else None
    )

@router.delete("/v1/tenant/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a tenant.
    
    Args:
        tenant_id: Tenant ID
        db: Database session
        
    Returns:
        Success message
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    db.delete(tenant)
    db.commit()
    
    return {"message": f"Tenant '{tenant.name}' deleted successfully"}
