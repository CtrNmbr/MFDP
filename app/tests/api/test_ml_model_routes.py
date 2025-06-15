import json
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlmodel import Session, delete, select
from app.src.api import app
from app.src.base.constants import TaskStatus
from app.src.models.predict_task import PredictTask
from app.src.models.account_transaction import AccountTransaction
from app.src.models.account import Account
from app.src.models.user import User
from app.src.models.quality_prediction import QualityPrediction
from app.src.database.database import get_session, init_db
from app.src.services.crud.prediction import create_prediction
from app.src.services.transaction_service import TransactionService
from app.src.services.user_service import UserService
from app.src.services.account_service import (
    AccountService,
    DEFAULT_BALANCE,
    DEFAULT_COST,
)


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


@pytest.fixture(autouse=True)
def mock_rabbitmq():
    with patch("pika.BlockingConnection") as mock_connection, patch(
        "app.src.services.rabbitmq_task_service.send_task_to_queue"
    ) as mock_send:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        yield mock_send


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


@pytest.fixture
def account_service():
    return AccountService(TransactionService())


def test_predict(db_session: Session, authenticated_user, account_service):
    user_id = UserService.verify_token(authenticated_user["token"])
    account = account_service.get_account_with_transactions(user_id, db_session)

    prediction_request = {
    "fixed acidity":12.8,
    "volatile acidity": 0.3,
    "citric acid": 0.74,
    "residual sugar": 2.6,
    "chlorides": 0.095,
    "free sulfur dioxide": 5.9,
    "total sulfur dioxide": 0.1,
    "density": 0.2,
    "pH": 1.3,
    "sulphates": 0.5,
    "alcohol": 0.4
    }
    expected_cost = account.cost_per_object

    assert account.balance == DEFAULT_BALANCE

    response = client.post(
        "/model/predict", json=prediction_request, headers=authenticated_user["headers"]
    )

    assert response.status_code == 200
    assert "task_id" in response.json()

    # Проверяем, что задача создана в БД
    task_id = response.json()["task_id"]
    task = db_session.exec(select(PredictTask).where(PredictTask.id == task_id)).first()
    assert task is not None
    assert task.status == TaskStatus.CREATED
    assert task.fixed_acidity == prediction_request["fixed acidity"]
    assert task.volatile_acidity == prediction_request["volatile acidity"]
    assert task.citric_acid == prediction_request["citric acid"]
    assert task.residual_sugar == prediction_request["residual sugar"]
    assert task.chlorides == prediction_request["chlorides"]
    assert task.free_sulfur_dioxide == prediction_request["free sulfur dioxide"]
    assert task.total_sulfur_dioxide == prediction_request["total sulfur dioxide"]
    assert task.density == prediction_request["density"]
    assert task.pH == prediction_request["pH"]
    assert task.sulphates == prediction_request["sulphates"]
    assert task.alcohol == prediction_request["alcohol"]

    db_session.refresh(account)
    assert account.balance == DEFAULT_BALANCE - expected_cost


def test_get_task(db_session: Session, authenticated_user, account_service):
    prediction_request = {
    "fixed acidity":12.8,
    "volatile acidity": 0.3,
    "citric acid": 0.74,
    "residual sugar": 2.6,
    "chlorides": 0.095,
    "free sulfur dioxide": 5.9,
    "total sulfur dioxide": 0.1,
    "density": 0.2,
    "pH": 1.3,
    "sulphates": 0.5,
    "alcohol": 0.4
    }
    expected_cost = DEFAULT_COST

    user_id = UserService.verify_token(authenticated_user["token"])
    account = account_service.get_account_with_transactions(user_id, db_session)
    assert account.balance == DEFAULT_BALANCE

    response = client.post(
        "/model/predict", json=prediction_request, headers=authenticated_user["headers"]
    )
    task_id = response.json()["task_id"]

    db_session.refresh(account)
    assert account.balance == DEFAULT_BALANCE - expected_cost

    # Получаем информацию о задаче
    response = client.get(
        f"/model/predictResult/{task_id}", headers=authenticated_user["headers"]
    )
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == str(task_id)
    assert result["status"] == TaskStatus.CREATED
    assert result["fixed acidity"] == prediction_request["fixed acidity"]
    assert result["volatile acidity"] == prediction_request["volatile acidity"]
    assert result["citric acid"] == prediction_request["citric acid"]
    assert result["residual sugar"] == prediction_request["residual sugar"]
    assert result["chlorides"] == prediction_request["chlorides"]
    assert result["free sulfur dioxide"] == prediction_request["free sulfur dioxide"]
    assert result["total sulfur dioxide"] == prediction_request["total sulfur dioxide"]
    assert result["density"] == prediction_request["density"]
    assert result["pH"] == prediction_request["pH"]
    assert result["sulphates"] == prediction_request["sulphates"]
    assert result["alcohol"] == prediction_request["alcohol"]


def test_get_prediction_history(db_session: Session, authenticated_user):
    user_id = UserService.verify_token(authenticated_user["token"])

    test_predictions = [
        QualityPrediction(
            user_id=user_id,
            fixed_acidity=12.8,
            volatile_acidity=0.3,
            citric_acid=0.74,
            residual_sugar=2.6,
            chlorides=0.095,
            free_sulfur_dioxide=5.9,
            total_sulfur_dioxide=0.1,
            density=0.2,
            pH=1.3,
            sulphates=0.5,
            alcohol=0.4,
            predicted_quality=5.19,
            created_at=datetime.now(timezone.utc),
        ),
        QualityPrediction(
            user_id=user_id,
            fixed_acidity=2.8,
            volatile_acidity=1.3,
            citric_acid=9.74,
            residual_sugar=12.6,
            chlorides=9.5,
            free_sulfur_dioxide=1.9,
            total_sulfur_dioxide=7.1,
            density=5.2,
            pH=6.3,
            sulphates=3.5,
            alcohol=4.4,
            predicted_quality=1.2,
            created_at=datetime.now(timezone.utc),
        ),
    ]

    for prediction in test_predictions:
        create_prediction(prediction, db_session)

    response = client.get("/model/history", headers=authenticated_user["headers"])
    assert response.status_code == 200
    predictions = response.json()
    assert isinstance(predictions, list)
    assert len(predictions) == 2

    for pred in predictions:
        assert "id" in pred
        assert "fixed_acidity" in pred
        assert "volatile_acidity" in pred
        assert "citric_acid" in pred
        assert "residual_sugar" in pred
        assert "chlorides" in pred
        assert "free_sulfur_dioxide" in pred
        assert "total_sulfur_dioxide" in pred
        assert "density" in pred
        assert "sulphates" in pred
        assert "alcohol" in pred
        assert "predicted_quality" in pred
        assert "created_at" in pred


def test_predict_unauthorized():
    prediction_request = {
    "fixed acidity":12.8,
    "volatile acidity": 0.3,
    "citric acid": 0.74,
    "residual sugar": 2.6,
    "chlorides": 0.095,
    "free sulfur dioxide": 5.9,
    "total sulfur dioxide": 0.1,
    "density": 0.2,
    "pH": 1.3,
    "sulphates": 0.5,
    "alcohol": 0.4
    }
    response = client.post("/model/predict", json=prediction_request)
    assert response.status_code == 401


def test_get_task_unauthorized():
    task_id = "550e8400-e29b-41d4-a716-446655440000"
    response = client.get(f"/model/predictResult/{task_id}")
    assert response.status_code == 401


def test_get_prediction_history_unauthorized():
    response = client.get("/model/history")
    assert response.status_code == 401


@pytest.fixture(autouse=True)
def cleanup_database(db_session: Session):
    yield
    # Очищаем все таблицы каскадно после каждого теста
    db_session.exec(delete(PredictTask))
    db_session.exec(delete(QualityPrediction))
    db_session.exec(delete(AccountTransaction))
    db_session.exec(delete(Account))
    db_session.exec(delete(User))
    db_session.commit()
