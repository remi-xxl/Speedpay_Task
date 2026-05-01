

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.models import TransactionType




class UserRegister(BaseModel):
   
    full_name: str = Field(..., min_length=2, max_length=100, examples=["Ada Lovelace"])
    email: EmailStr = Field(..., examples=["ada@example.com"])
  
    password: str = Field(..., min_length=8, examples=["securepass123"])


class UserLogin(BaseModel):
   
    email: EmailStr
    password: str


class Token(BaseModel):
   
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    
    user_id: Optional[int] = None



class UserResponse(BaseModel):
   
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
  
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    account_number: str



class DepositRequest(BaseModel):
  
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[500.00])
    description: Optional[str] = Field(None, max_length=255, examples=["Salary deposit"])


class WithdrawRequest(BaseModel):
    
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[200.00])
    description: Optional[str] = Field(None, max_length=255, examples=["ATM withdrawal"])


class TransferRequest(BaseModel):
  
   
    recipient_account_number: str = Field(..., min_length=6, max_length=6, examples=["483920"])
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[100.00])
    description: Optional[str] = Field(None, max_length=255, examples=["Splitting the bill"])


class BalanceResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    account_number: str
    balance: Decimal

class TransactionResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_type: TransactionType
    amount: Decimal
    balance_after: Decimal
    description: Optional[str]
    created_at: datetime


class WalletOperationResponse(BaseModel):
   
    message: str
    transaction: TransactionResponse
    new_balance: Decimal