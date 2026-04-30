

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="Get all users (Admin only)",
    description="Retrieve a list of all registered users with their details and balances.",
)
def get_all_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users