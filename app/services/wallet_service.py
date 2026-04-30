
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Transaction, TransactionType, User


class WalletService:


    def __init__(self, db: Session):
    
        self.db = db

    def get_balance(self, user_id: int) -> float:
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.balance


    def deposit(self, user: User, amount: Decimal, description: str | None) -> Transaction:
        # Update the balance in memory (SQLAlchemy tracks this change).
        user.balance = Decimal(str(user.balance)) + amount

        # Build the transaction record.
        txn = Transaction(
            sender_id=user.id,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            balance_after=user.balance,
            description=description,
        )

        self.db.add(txn)
        self.db.commit()          # write both the balance update and the new row
        self.db.refresh(txn)      # reload the row to get DB-generated fields (id, created_at)
        self.db.refresh(user)     # ensure user.balance reflects the committed value
        return txn

    # -----------------------------------------------------------------------
    # WITHDRAW
    # -----------------------------------------------------------------------

    def withdraw(self, user: User, amount: Decimal, description: str | None) -> Transaction:
        current_balance = Decimal(str(user.balance))

        if amount > current_balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient funds. Available balance: {current_balance:.2f}",
            )

        user.balance = current_balance - amount

        txn = Transaction(
            sender_id=user.id,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount,
            balance_after=user.balance,
            description=description,
        )

        self.db.add(txn)
        self.db.commit()
        self.db.refresh(txn)
        self.db.refresh(user)
        return txn

   

    def transfer(
        self,
        sender: User,
        recipient_account_number: str,
        amount: Decimal,
        description: str | None,
    ) -> Transaction:
       #ACID compliant 
        # ── Rule 1: no self-transfers ──────────────────────────────────────
        if sender.account_number == recipient_account_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot transfer funds to your own account.",
            )

        # ── Rule 2: recipient must exist ───────────────────────────────────
        recipient = (
            self.db.query(User)
            .filter(User.account_number == recipient_account_number)
            .first()
        )
        if not recipient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user found with account number {recipient_account_number}.",
            )

        # ── Rule 3: sufficient funds ───────────────────────────────────────
        sender_balance = Decimal(str(sender.balance))
        if amount > sender_balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient funds. Available balance: {sender_balance:.2f}",
            )

        # ── Update balances ────────────────────────────────────────────────
        sender.balance = sender_balance - amount
        recipient.balance = Decimal(str(recipient.balance)) + amount

        # ── Write sender's transaction (TRANSFER_OUT) ──────────────────────
        sender_txn = Transaction(
            sender_id=sender.id,
            recipient_id=recipient.id,
            transaction_type=TransactionType.TRANSFER_OUT,
            amount=amount,
            balance_after=sender.balance,
            description=description,
        )

        # ── Write recipient's transaction (TRANSFER_IN) ────────────────────
        recipient_txn = Transaction(
            sender_id=recipient.id,     
            recipient_id=sender.id,
            transaction_type=TransactionType.TRANSFER_IN,
            amount=amount,
            balance_after=recipient.balance,
            description=description,
        )

        self.db.add(sender_txn)
        self.db.add(recipient_txn)

        self.db.commit()
        self.db.refresh(sender_txn)
        self.db.refresh(sender)
        return sender_txn