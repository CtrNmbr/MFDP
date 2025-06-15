import pytest
from fastapi.testclient import TestClient
from app.src.api import app
from app.src.database.database import get_session, init_db
from app.src.models.account import Account
from app.src.models.account_transaction import AccountTransaction
from app.src.models.user import User
from sqlmodel import Session, delete, select

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


def test_signup_success(db_session: Session, test_user_data):
    response = client.post("/user/signup", json=test_user_data)

    assert response.status_code == 200
    assert response.json() == {"message": "User successfully registered!"}

    # Проверяем, что пользователь действительно создан в БД
    user = db_session.exec(
        select(User).where(User.email == test_user_data["email"])
    ).first()
    assert user is not None
    assert user.email == test_user_data["email"]


def test_signup_duplicate_email(db_session: Session, test_user_data):
    # Первая регистрация
    client.post("/user/signup", json=test_user_data)

    # Пытаемся зарегистрировать того же пользователя
    response = client.post("/user/signup", json=test_user_data)

    assert response.status_code == 409
    assert "User with supplied username exists" in response.json()["detail"]


def test_signin_success(db_session: Session, test_user_data):
    # Сначала регистрируем пользователя
    client.post("/user/signup", json=test_user_data)

    # Пытаемся войти
    response = client.post("/user/signin", json=test_user_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_signin_wrong_password(db_session: Session, test_user_data):
    # Регистрируем пользователя
    client.post("/user/signup", json=test_user_data)

    # Пытаемся войти с неверным паролем
    wrong_password_data = test_user_data.copy()
    wrong_password_data["password"] = "wrong_password"

    response = client.post("/user/signin", json=wrong_password_data)

    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_signin_nonexistent_user(db_session: Session):
    response = client.post(
        "/user/signin",
        json={"email": "nonexistent@example.com", "password": "some_password"},
    )

    assert response.status_code == 404
    assert "User does not exist" in response.json()["detail"]


@pytest.fixture(autouse=True)
def cleanup_database(db_session: Session):
    yield
    # Очищаем все таблицы каскадно после каждого теста
    db_session.exec(delete(AccountTransaction))
    db_session.exec(delete(Account))
    db_session.exec(delete(User))

    db_session.commit()
