import pytest
from fastapi.testclient import TestClient
from app.src.api import app
from app.src.database.database import get_session, init_db
from app.src.models.account import Account
from app.src.models.account_transaction import AccountTransaction
from app.src.models.user import User
from sqlmodel import Session, delete

from app.src.services.account_service import DEFAULT_BALANCE

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()
    yield


@pytest.fixture
def db_session():
    session = next(get_session())
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user_data():
    return {"email": "test@example.com", "password": "test_password123"}


@pytest.fixture
def authenticated_user(db_session: Session, test_user_data):
    # Регистрируем пользователя
    client.post("/user/signup", json=test_user_data)

    # Выполняем вход и получаем токен
    response = client.post("/user/signin", json=test_user_data)
    token = response.json()["access_token"]

    return {"token": token, "headers": {"Authorization": f"Bearer {token}"}}


def test_get_account_details(db_session: Session, authenticated_user):
    response = client.get("/account/details", headers=authenticated_user["headers"])

    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert data["balance"] == DEFAULT_BALANCE
    assert "user_id" in data
    assert "transactions" in data
    assert isinstance(data["transactions"], list)


def test_get_account_details_unauthorized():
    response = client.get("/account/details")
    assert response.status_code == 401


def test_add_funds_success(db_session: Session, authenticated_user):
    fund_data = {"amount": 1000.0}
    response = client.post(
        "/account/fund", headers=authenticated_user["headers"], json=fund_data
    )

    assert response.status_code == 200

    # Проверяем, что средства действительно добавлены
    details_response = client.get(
        "/account/details", headers=authenticated_user["headers"]
    )
    assert details_response.json()["balance"] - DEFAULT_BALANCE == 1000.0


def test_add_funds_unauthorized():
    fund_data = {"amount": 1000.0}
    response = client.post("/account/fund", json=fund_data)
    assert response.status_code == 401


def test_add_negative_funds(db_session: Session, authenticated_user):
    fund_data = {"amount": -1000.0}
    response = client.post(
        "/account/fund", headers=authenticated_user["headers"], json=fund_data
    )

    assert response.status_code == 400


@pytest.fixture(autouse=True)
def cleanup_database(db_session: Session):
    yield
    # Очищаем все таблицы каскадно после каждого теста
    db_session.exec(delete(AccountTransaction))
    db_session.exec(delete(Account))
    db_session.exec(delete(User))
    db_session.commit()
