import pytest
from datetime import datetime, timedelta
from sqlmodel import Session, SQLModel, create_engine
from app.src.services.user_service import UserService, hash_password
from app.src.base.constants import UserRole


# Создаем тестовую БД в памяти
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
def user_service():
    return UserService()


def test_hash_password():
    password = "test_password"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert len(hashed) > 0
    assert hashed != password

    # Проверяем идемпотентность
    assert hash_password(password) == hashed


def test_make_user(session, user_service):
    email = "test@example.com"
    password = "test_password"

    user = user_service.make_user(email, password, session)

    assert user.email == email
    assert user.password_hash == hash_password(password)
    assert user.role == UserRole.USER
    assert isinstance(user.last_update_datetime, datetime)


def test_create_duplicate_user(session, user_service):
    email = "test@example.com"
    password = "test_password"

    # Создаем первого пользователя
    user_service.make_user(email, password, session)

    # Пробуем создать дубликат
    result = user_service.make_user(email, password, session)

    assert isinstance(result, dict)
    assert result["status"] is False
    assert "User exists" in result["message"]


def test_get_user_by_email(session, user_service):
    email = "test@example.com"
    password = "test_password"

    created_user = user_service.make_user(email, password, session)
    found_user = user_service.get_user_by_email(email, session)

    assert found_user is not None
    assert found_user.email == email
    assert found_user.id == created_user.id


def test_get_user_by_id(session, user_service):
    email = "test@example.com"
    password = "test_password"

    created_user = user_service.make_user(email, password, session)
    found_user = user_service.get_user_by_id(created_user.id, session)

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == email


def test_check_credentials():
    password = "test_password"
    hashed_password = hash_password(password)

    assert UserService.check_credentials(password, hashed_password) is True
    assert UserService.check_credentials("wrong_password", hashed_password) is False


def test_create_token():
    test_data = {"subscriber": "123", "email": "test@example.com"}
    token = UserService.create_token(test_data)

    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token():
    test_data = {"subscriber": "123", "email": "test@example.com"}
    token = UserService.create_token(test_data)

    user_id = UserService.verify_token(token)
    assert user_id == "123"


def test_verify_invalid_token():
    invalid_token = "invalid.token.string"
    result = UserService.verify_token(invalid_token)
    assert result is None


def test_token_expiration():
    test_data = {"subscriber": "123"}
    # Создаем токен с очень коротким временем жизни
    token = UserService.create_token(
        test_data, expires_delta=timedelta(microseconds=1)
    )

    # Ждем, пока токен истечет
    import time

    time.sleep(1)

    result = UserService.verify_token(token)
    assert result is None
