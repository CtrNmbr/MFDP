import pytest
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine
from app.src.services.crud.prediction import get_predictions, create_prediction
from app.src.models.quality_prediction import QualityPrediction
from app.src.models.user import User, UserRole


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
def test_user(session):
    user = User(
        email="test@example.com",
        password_hash="test_hash",
        role=UserRole.USER,
        last_update_datetime=datetime.now(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_create_prediction(session, test_user):
    prediction_data = QualityPrediction(
        user_id=test_user.id,
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
        created_at=datetime.now()
    )

    created_prediction = create_prediction(prediction_data, session)

    assert created_prediction.user_id == test_user.id
    assert created_prediction.fixed_acidity == prediction_data.fixed_acidity
    assert created_prediction.volatile_acidity == prediction_data.volatile_acidity
    assert created_prediction.citric_acid == prediction_data.citric_acid
    assert created_prediction.residual_sugar == prediction_data.residual_sugar
    assert created_prediction.chlorides == prediction_data.chlorides
    assert created_prediction.free_sulfur_dioxide == prediction_data.free_sulfur_dioxide
    assert created_prediction.total_sulfur_dioxide == prediction_data.total_sulfur_dioxide
    assert created_prediction.density == prediction_data.density
    assert created_prediction.pH == prediction_data.pH
    assert created_prediction.sulphates == prediction_data.sulphates
    assert created_prediction.alcohol == prediction_data.alcohol
    assert isinstance(created_prediction.created_at, datetime)
    assert created_prediction.user == test_user


def test_get_predictions_by_user_id(session, test_user):
    # Создаем несколько предсказаний для тестового пользователя
    prediction_1 = QualityPrediction(
        user_id=test_user.id,
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
        created_at=datetime.now()
    )
    prediction_2 = QualityPrediction(
        user_id=test_user.id,
        fixed_acidity=2.8,
        volatile_acidity=.3,
        citric_acid=3.74,
        residual_sugar=.6,
        chlorides=5.095,
        free_sulfur_dioxide=6.9,
        total_sulfur_dioxide=7.1,
        density=8.2,
        pH=9.3,
        sulphates=1.5,
        alcohol=2.4,
        predicted_quality=3.19,
        created_at=datetime.now()
    )

    # Создаем другого пользователя и предсказание для него
    other_user = User(
        email="other@example.com",
        password_hash="other_hash",
        role=UserRole.USER,
        last_update_datetime=datetime.now(),
    )
    session.add(other_user)
    session.commit()

    other_prediction = QualityPrediction(
        user_id=other_user.id,
        fixed_acidity=1.8,
        volatile_acidity=9.3,
        citric_acid=8.74,
        residual_sugar=7.6,
        chlorides=6.095,
        free_sulfur_dioxide=5.9,
        total_sulfur_dioxide=4.1,
        density=3.2,
        pH=2.3,
        sulphates=1.5,
        alcohol=2.4,
        predicted_quality=9.19,
        created_at=datetime.now()
    )

    create_prediction(prediction_1, session)
    create_prediction(prediction_2, session)
    create_prediction(other_prediction, session)

    # Получаем все предсказания пользователя
    predictions = get_predictions(test_user.id, session)

    assert len(predictions) == 2
    assert all(p.user_id == test_user.id for p in predictions)
    assert all(isinstance(p.created_at, datetime) for p in predictions)
    assert all(p.user == test_user for p in predictions)


def test_get_predictions_empty_result(session):
    non_existent_user_id = 999
    predictions = get_predictions(non_existent_user_id, session)

    assert len(predictions) == 0
    assert isinstance(predictions, list)
