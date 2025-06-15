import pytest
from datetime import datetime, timezone
from sqlmodel import Session, SQLModel, create_engine
from app.src.services.transaction_service import TransactionService
from app.src.models.account_transaction import AccountTransaction
from app.src.base.constants import TransactionType


@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture
def transaction_service():
    return TransactionService()


def test_modify_balance_transaction_deposit(session, transaction_service):
    # Тест депозита (положительная сумма)
    amount = 1000
    account_id = 1

    transaction = transaction_service.modify_balance_transaction(
        amount, account_id, session
    )

    assert transaction.type == TransactionType.DEPOSIT
    assert transaction.amount == amount
    assert transaction.account_id == account_id
    assert isinstance(transaction.created_at, datetime)


def test_modify_balance_transaction_withdraw(session, transaction_service):
    # Тест снятия (отрицательная сумма)
    amount = -500
    account_id = 1

    transaction = transaction_service.modify_balance_transaction(
        amount, account_id, session
    )

    assert transaction.type == TransactionType.WITHDRAW
    assert transaction.amount == amount
    assert transaction.account_id == account_id
    assert isinstance(transaction.created_at, datetime)
