

import random
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey,
    Integer, Numeric, String,
)
from sqlalchemy.orm import relationship
import enum

from app.database import Base



class TransactionType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER_OUT = "TRANSFER_OUT"  
    TRANSFER_IN = "TRANSFER_IN"     



class User(Base):
   
    __tablename__ = "users"

    
    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

  
    email = Column(String(255), unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

   
    account_number = Column(String(6), unique=True, index=True, nullable=False)


    balance = Column(Numeric(12, 2), default=0.00, nullable=False)

    
    is_admin = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    
    transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender",
    )



class Transaction(Base):
   
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    transaction_type = Column(Enum(TransactionType), nullable=False)

    
    amount = Column(Numeric(12, 2), nullable=False)

   
    balance_after = Column(Numeric(12, 2), nullable=False)

    
    description = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="transactions"
    )
    recipient = relationship(
        "User", foreign_keys=[recipient_id]
    )



def generate_account_number() -> str:
   
    return str(random.randint(100000, 999999))