
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.schemas import Token, UserRegister, UserResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Creates a new wallet account. A unique 6-digit account number is "
        "generated automatically. Returns the user profile (no password)."
    ),
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
  
    service = AuthService(db)
    new_user = service.register(user_data)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Log in and receive a JWT",
    description=(
        "Accepts email + password. Returns an access token to use as "
        "'Authorization: Bearer <token>' on all protected endpoints."
    ),
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
   
    service = AuthService(db)
    token = service.login(user_data.email, user_data.password)
    return token