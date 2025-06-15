from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.src.models.account import Account
from app.src.services.transaction_service import TransactionService

DEFAULT_BALANCE = 50
DEFAULT_COST = 1


class AccountService:
    def __init__(self,
                 transaction_service: TransactionService
                 ):
        self._transaction_service = transaction_service

    def create_account(self,
                       user_id: int,
                       session: Session
                       ) -> Account:
        account = Account(
            user_id=user_id,
            balance=DEFAULT_BALANCE,
            cost_per_object=DEFAULT_COST,
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        return account

    def __change_balance(self,
                         account: Account,
                         amount_w_sign: int,
                         session: Session
                         ):
        account.change_balance(amount_w_sign)
        self._transaction_service.modify_balance_transaction(
            amount=amount_w_sign, account_id=account.id, session=session
        )

    @staticmethod
    def __get_account(user_id: int,
                      session: Session
                      ) -> Account:
        statement = select(Account).where(Account.user_id == user_id)
        return session.exec(statement).first()

    def fund(self, user_id: int, amount: int, session: Session):
        assert amount > 0
        account = self.__get_account(user_id, session)
        self.__change_balance(account, amount, session)
        session.commit()

    def refund(self, user_id: int, amount: int, session: Session):
        account = self.__get_account(user_id, session)
        if amount > account.balance:
            return {"message": "Not enough balance", "status": False}
        self.__change_balance(account, -amount, session)
        session.commit()

    def create_payment(self, user_id: int, session: Session):
        account = self.__get_account(user_id, session)
        payment_sum = account.cost_per_object
        if payment_sum > account.balance:
            return {"message": "Not enough balance", "status": False}
        account.change_balance(-payment_sum)
        transaction = self._transaction_service.create_transaction(
            payment_sum, account_id=account.id, session=session
        )
        session.commit()
        return transaction

    def cancel_payment(self, user_id: int, session: Session):
        account = self.__get_account(user_id, session)
        payment_sum = account.cost_per_object
        #transaction = self._transaction_manager.create_transaction(
        #    -payment_sum, account_id=account.id, session=session
        #)
        transaction = self._transaction_manager.modify_balance_transaction(
            payment_sum, account_id=account.id, session=session
        )#DEPOSIT
        # возврат новой транзакцией
        account.change_balance(transaction.amount)
        session.commit()

        return transaction

    def get_account_with_transactions(self, user_id: int, session: Session):
        statement = (
            select(Account)
            .options(selectinload(Account.transactions))
            .where(Account.user_id == user_id)
        )
        account = session.exec(statement).first()
        return account
