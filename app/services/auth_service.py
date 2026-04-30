

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.models import User, generate_account_number
from app.schemas.schemas import Token, UserResponse


class AuthService:
   

    def __init__(self, db: Session):
        self.db = db

    def register(self, user_data) -> User:
       
        # Check email uniqueness
        existing = self.db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        # Generate unique account number
        while True:
            account_number = generate_account_number()
            if not self.db.query(User).filter(User.account_number == account_number).first():
                break

        # Create user
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            account_number=account_number,
            balance=0.00,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def login(self, email: str, password: str) -> Token:
      
        user = self.db.query(User).filter(User.email == email).first()

        invalid_credentials = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not user:
            raise invalid_credentials

        if not verify_password(password, user.hashed_password):
            raise invalid_credentials

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account has been deactivated.",
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")