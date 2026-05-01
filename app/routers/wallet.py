

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import (
    BalanceResponse,
    DepositRequest,
    TransferRequest,
    WalletOperationResponse,
    WithdrawRequest,
)
from app.services.wallet_service import WalletService

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.post(
    "/deposit",
    response_model=WalletOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Deposit funds into your account",
)
def deposit(
    body: DepositRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),   # ← auth check happens here
):
  
    service = WalletService(db)
    txn = service.deposit(current_user, body.amount, body.description)

    return WalletOperationResponse(
        message="Deposit successful.",
        transaction=txn,
        new_balance=current_user.balance,
    )


@router.post(
    "/withdraw",
    response_model=WalletOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Withdraw funds from your account",
)
def withdraw(
    body: WithdrawRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    service = WalletService(db)
    txn = service.withdraw(current_user, body.amount, body.description)

    return WalletOperationResponse(
        message="Withdrawal successful.",
        transaction=txn,
        new_balance=current_user.balance,
    )


@router.get(
    "/balance",
    response_model=BalanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Check your current balance",
)
def get_balance(
    current_user: User = Depends(get_current_user),
):
   
    return BalanceResponse(
        account_number=current_user.account_number,
        balance=current_user.balance,
    )


@router.post(
    "/transfer",
    response_model=WalletOperationResponse,
    status_code=status.HTTP_200_OK,
    summary="Transfer funds to another user",
)
def transfer(
    body: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    service = WalletService(db)
    txn = service.transfer(
        sender=current_user,
        recipient_account_number=body.recipient_account_number,
        amount=body.amount,
        description=body.description,
    )

    return WalletOperationResponse(
        message=f"Transfer of {body.amount:.2f} to account {body.recipient_account_number} successful.",
        transaction=txn,
        new_balance=current_user.balance,
    )