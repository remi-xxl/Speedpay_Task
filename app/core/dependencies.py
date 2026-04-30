

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        # WWW-Authenticate header tells the client how to authenticate.
        headers={"WWW-Authenticate": "Bearer"},
    )

    # decode_access_token returns None if the token is bad.
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # "sub" (subject) is where we stored the user's ID as a string.
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Look up the user in the database.
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    # Reject deactivated accounts.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deactivated",
        )

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency: same as get_current_user, but also requires is_admin == True.

    Raises HTTP 403 if the authenticated user is not an admin.
    Chain it after get_current_user so we don't duplicate the token logic.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user