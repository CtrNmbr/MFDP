from app.src.services.account_service import (AccountService, DEFAULT_BALANCE, DEFAULT_COST)
from app.src.services.transaction_service import TransactionService
from sqlmodel import Session, SQLModel, create_engine
import pytest

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

@pytest.fixture
def account_service(transaction_service):
    return AccountService(transaction_service)

def test_create_account(session, account_service):
    user_id = 1

    account = account_service.create_account(user_id, session)

    assert account.user_id == user_id
    assert account.balance == DEFAULT_BALANCE
    assert account.cost_per_object == DEFAULT_COST

def test_fund_account(session, account_service):
    user_id = 1
    initial_amount = 1000

    # Создаем аккаунт
    account_service.create_account(user_id, session)

    # Пополняем баланс
    account_service.fund(user_id, initial_amount, session)

    updated_account = account_service._AccountService__get_account(user_id, session)
    assert updated_account.balance == DEFAULT_BALANCE + initial_amount

def test_refund_success(session, account_service):
    user_id = 1
    initial_amount = 1000
    refund_amount = 500

    # Создаем и пополняем аккаунт
    account_service.create_account(user_id, session)
    account_service.fund(user_id, initial_amount, session)

    # Делаем возврат
    result = account_service.refund(user_id, refund_amount, session)

    updated_account = account_service._AccountService__get_account(user_id, session)
    assert updated_account.balance == DEFAULT_BALANCE + initial_amount - refund_amount
    assert result is None

def test_refund_insufficient_balance(session, account_service):
    user_id = 1
    initial_amount = 100
    refund_amount = 500

    # Создаем и пополняем аккаунт
    account_service.create_account(user_id, session)
    account_service.fund(user_id, initial_amount, session)

    # Пробуем сделать возврат большей суммы
    result = account_service.refund(user_id, refund_amount, session)

    assert result["status"] is False
    assert "Not enough balance" in result["message"]

def test_payment_insufficient_balance(session, account_service):
    user_id = 1
    initial_amount = 0.1

    # Создаем и пополняем аккаунт
    account_service.create_account(user_id, session)
    account_service.fund(user_id, initial_amount, session)

    # Пробуем создать холд
    result = account_service.create_payment(user_id, session)

    assert result["status"] is False
    assert "Not enough balance" in result["message"]

def test_create_payment(session, account_service):
    user_id = 1
    initial_amount = 1000

    # Создаем и пополняем аккаунт
    account = account_service.create_account(user_id, session)
    account_service.fund(user_id, initial_amount, session)

    # Создаем и завершаем платеж
    completed_transaction = account_service.create_payment(user_id, session)

    updated_account = account_service._AccountService__get_account(user_id, session)
    expected_payment = account.cost_per_object

    assert completed_transaction is not None
    assert (
        updated_account.balance == DEFAULT_BALANCE + initial_amount - expected_payment
    )

def test_get_account_with_transactions(session, account_service):
    user_id = 1
    initial_amount = 1000

    # Создаем и пополняем аккаунт
    account = account_service.create_account(user_id, session)
    account_service.fund(user_id, initial_amount, session)

    # Получаем аккаунт с транзакциями
    account_with_transactions = account_service.get_account_with_transactions(
        user_id, session
    )

    assert account_with_transactions is not None
    assert account_with_transactions.id == account.id
    assert len(account_with_transactions.transactions) > 0
