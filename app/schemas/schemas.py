

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.models import TransactionType




class UserRegister(BaseModel):
    """Body sent by the client when creating a new account."""
    full_name: str = Field(..., min_length=2, max_length=100, examples=["Ada Lovelace"])
    email: EmailStr = Field(..., examples=["ada@example.com"])
  
    password: str = Field(..., min_length=8, examples=["securepass123"])


class UserLogin(BaseModel):
    """Body sent when logging in."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Returned after a successful login."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """The decoded payload we store inside the JWT."""
    user_id: Optional[int] = None



class UserResponse(BaseModel):
    """
    What we send back when a user is returned from any endpoint.
    Notice: hashed_password is NOT here — it never leaves the server.
    """
    model_config = ConfigDict(from_attributes=True)  

    id: int
    full_name: str
    email: EmailStr
    account_number: str
    balance: Decimal
    is_admin: bool
    is_active: bool
    created_at: datetime


class UserPublicResponse(BaseModel):
    """
    Minimal user info returned when looking up a transfer recipient.
    We don't expose balance or email to other users.
    """
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    account_number: str



class DepositRequest(BaseModel):
    """Body for POST /wallet/deposit"""
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[500.00])
    description: Optional[str] = Field(None, max_length=255, examples=["Salary deposit"])


class WithdrawRequest(BaseModel):
    """Body for POST /wallet/withdraw"""
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[200.00])
    description: Optional[str] = Field(None, max_length=255, examples=["ATM withdrawal"])


class TransferRequest(BaseModel):
    """Body for POST /wallet/transfer"""
    # Recipients are identified by their account number, not their ID.
    # This mirrors how real banking apps work and avoids exposing internal IDs.
    recipient_account_number: str = Field(..., min_length=6, max_length=6, examples=["483920"])
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[100.00])
    description: Optional[str] = Field(None, max_length=255, examples=["Splitting the bill"])


class BalanceResponse(BaseModel):
    """Body returned by GET /wallet/balance"""
    model_config = ConfigDict(from_attributes=True)

    account_number: str
    balance: Decimal

class TransactionResponse(BaseModel):
    """Represents a single transaction entry (used in lists and receipts)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_type: TransactionType
    amount: Decimal
    balance_after: Decimal
    description: Optional[str]
    created_at: datetime


class WalletOperationResponse(BaseModel):
    """
    Generic response returned after any successful wallet operation
    (deposit, withdrawal, or transfer).
    """
    message: str
    transaction: TransactionResponse
    new_balance: Decimal