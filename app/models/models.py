

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
    """
    Represents a registered user of the wallet system.

    __tablename__ tells SQLAlchemy what to call the table in PostgreSQL.
    """
    __tablename__ = "users"

    # Primary key — PostgreSQL auto-increments this integer.
    id = Column(Integer, primary_key=True, index=True)

    # The user's chosen display name. Not unique — two people can share a name.
    full_name = Column(String(100), nullable=False)

    # Email is used as the login identifier and must be unique.
    email = Column(String(255), unique=True, index=True, nullable=False)

    # We NEVER store the raw password. passlib turns it into a bcrypt hash
    # (e.g. "$2b$12$...") and stores that instead.
    hashed_password = Column(String, nullable=False)

    # 6-digit account number, e.g. "483920". Unique per user.
    # We generate this in Python (see generate_account_number below) rather
    # than relying on the database, so we can guarantee uniqueness easily.
    account_number = Column(String(6), unique=True, index=True, nullable=False)

    # Current wallet balance.
    # Numeric(12, 2) → up to 12 digits total, 2 after the decimal point.
    # NEVER use Float for money — floats have rounding errors.
    balance = Column(Numeric(12, 2), default=0.00, nullable=False)

    # Admins can see all users; regular users see only themselves.
    is_admin = Column(Boolean, default=False, nullable=False)

    # Whether the account is active. We can deactivate instead of deleting.
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamp automatically set when the row is inserted.
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # SQLAlchemy relationship — lets us write user.transactions in Python
    # instead of joining tables manually. "back_populates" means Transaction
    # also gets a .user attribute pointing back here.
    transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender",
    )



class Transaction(Base):
    """
    Records every money movement: deposits, withdrawals, and transfers.

    For transfers we write TWO rows — one TRANSFER_OUT on the sender and one
    TRANSFER_IN on the recipient — so each user's statement is self-contained.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Which user initiated this transaction (or, for TRANSFER_IN, who received).
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Only populated for transfers. NULL for deposits/withdrawals.
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # What kind of transaction is this?
    transaction_type = Column(Enum(TransactionType), nullable=False)

    # How much money moved. Always positive.
    amount = Column(Numeric(12, 2), nullable=False)

    # Snapshot of the sender's balance *after* this transaction completed.
    # Useful for building account statements without recalculating history.
    balance_after = Column(Numeric(12, 2), nullable=False)

    # Optional human-readable note (e.g. "Rent for June").
    description = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ORM relationships
    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="transactions"
    )
    recipient = relationship(
        "User", foreign_keys=[recipient_id]
    )



def generate_account_number() -> str:
   
    return str(random.randint(100000, 999999))