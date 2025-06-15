from app.src.base.constants import TransactionType
from app.src.models.account_transaction import AccountTransaction
from sqlmodel import Session, select
from datetime import timezone, datetime

class TransactionService:

    def modify_balance_transaction(self,
                                   amount: int,
                                   account_id: int,
                                   session: Session):

        transaction = AccountTransaction(
            type=(TransactionType.DEPOSIT
                  if amount > 0
                  else TransactionType.WITHDRAW),
            amount=amount,
            account_id=account_id,
            created_at=datetime.now(timezone.utc)
        )

        session.add(transaction)

        return transaction

    def create_transaction(self,
                                amount: int,
                                account_id: int,
                                session: Session):
        transaction = AccountTransaction(
            type=TransactionType.PAYMENT,
            amount=amount,
            account_id=account_id,
            created_at=datetime.now(timezone.utc),
        )

        session.add(transaction)

        return transaction
