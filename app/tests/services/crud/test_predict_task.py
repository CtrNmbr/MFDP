import pytest
import uuid
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine
from app.src.services.crud.predict_task import (
    create_predict_task,
    get_predict_task,
    update_predict_task,
    delete_predict_task,
    get_predict_tasks,
)
from app.src.models.predict_task import PredictTask
from app.src.models.user import User, UserRole
from app.src.base.constants import TaskStatus, TransactionType
from app.src.models.account import Account
from app.src.models.account_transaction import AccountTransaction


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


@pytest.fixture
def test_account(session, test_user):
    account = Account(
        user_id=test_user.id, balance=100, cost_per_object=1
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@pytest.fixture
def test_transaction(session, test_account):
    transaction = AccountTransaction(
        type=TransactionType.PAYMENT,
        amount=100,
        account_id=test_account.id,
        created_at=datetime.now(),
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@pytest.fixture
def test_task(session, test_user, test_transaction):
    task = PredictTask(
        id=uuid.uuid4(),
        user_id=test_user.id,
        fixed_acidity=12.8,
        volatile_acidity= 0.3,
        citric_acid= 0.74,
        residual_sugar= 2.6,
        chlorides= 0.095,
        free_sulfur_dioxide= 5.9,
        total_sulfur_dioxide= 0.1,
        density= 0.2,
        pH= 1.3,
        sulphates= 0.5,
        alcohol= 0.4,
        status=TaskStatus.CREATED,
        predicted_result=None,
        account_transaction_id=test_transaction.id
    )
    return create_predict_task(task, session)


def test_create_predict_task(session, test_user):
    task_data = PredictTask(
        id=uuid.uuid4(),
        user_id=test_user.id,
        fixed_acidity=12.8,
        volatile_acidity= 0.3,
        citric_acid= 0.74,
        residual_sugar= 2.6,
        chlorides= 0.095,
        free_sulfur_dioxide= 5.9,
        total_sulfur_dioxide= 0.1,
        density= 0.2,
        pH= 1.3,
        sulphates= 0.5,
        alcohol= 0.4,
        status=TaskStatus.CREATED,
        predicted_result=None,
        account_transaction_id=1
    )

    created_task = create_predict_task(task_data, session)

    assert created_task.user_id == test_user.id
    assert created_task.status == TaskStatus.CREATED
    assert created_task.predicted_result is None
    assert created_task.fixed_acidity == 12.8
    assert created_task.volatile_acidity == 0.3
    assert created_task.citric_acid == 0.74
    assert created_task.residual_sugar == 2.6
    assert created_task.chlorides == 0.095
    assert created_task.free_sulfur_dioxide == 5.9
    assert created_task.total_sulfur_dioxide == 0.1
    assert created_task.density == 0.2
    assert created_task.pH == 1.3
    assert created_task.sulphates == 0.5
    assert created_task.alcohol == 0.4

def test_get_predict_task(session, test_task):
    retrieved_task = get_predict_task(test_task.id, session)

    assert retrieved_task.id == test_task.id
    assert retrieved_task.user_id == test_task.user_id
    assert retrieved_task.status == test_task.status


def test_get_predict_task_not_found(session):
    non_existent_id = uuid.uuid4()

    with pytest.raises(
        ValueError, match=f"PredictTask with id {non_existent_id} not found"
    ):
        get_predict_task(non_existent_id, session)


def test_update_predict_task(session, test_task):
    updated_data = PredictTask(
        id=test_task.id,
        user_id=test_task.user_id,
        fixed_acidity=test_task.fixed_acidity,
        volatile_acidity=test_task.volatile_acidity,
        citric_acid=test_task.citric_acid,
        residual_sugar=test_task.residual_sugar,
        chlorides=test_task.chlorides,
        free_sulfur_dioxide=test_task.free_sulfur_dioxide,
        total_sulfur_dioxide=test_task.total_sulfur_dioxide,
        density=test_task.density,
        pH=test_task.pH,
        sulphates=test_task.sulphates,
        alcohol=test_task.alcohol,
        status=TaskStatus.COMPLETED,
        predicted_result=5.19,
        account_transaction_id=test_task.account_transaction_id,
    )

    updated_task = update_predict_task(updated_data, session)

    assert updated_task.id == test_task.id
    assert updated_task.status == TaskStatus.COMPLETED
    assert updated_task.result == 5.19


def test_delete_predict_task(session, test_task):
    delete_predict_task(test_task.id, session)

    with pytest.raises(ValueError):
        get_predict_task(test_task.id, session)


@pytest.fixture
def test_tasks(session, test_user, test_transaction):
    tasks = []
    for status in [TaskStatus.CREATED, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]:
        task = PredictTask(
            id=uuid.uuid4(),
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
            status=status,
            predicted_quality=None,
            account_transaction_id=test_transaction.id,
        )
        tasks.append(create_predict_task(task, session))
    return tasks


def test_get_all_predict_tasks(session, test_tasks):
    all_tasks = get_predict_tasks(session)
    assert len(all_tasks) == 3


def test_get_predict_tasks_by_status(session, test_tasks):
    created_tasks = get_predict_tasks(session, status=TaskStatus.CREATED)
    assert len(created_tasks) == 1
    assert created_tasks[0].status == TaskStatus.CREATED


def test_get_predict_tasks_by_user(session, test_tasks, test_user):
    user_tasks = get_predict_tasks(session, user_id=test_user.id)
    assert len(user_tasks) == 3
    assert all(task.user_id == test_user.id for task in user_tasks)


def test_get_predict_tasks_with_limit(session, test_tasks):
    limited_tasks = get_predict_tasks(session, limit=2)
    assert len(limited_tasks) == 2


def test_get_predict_tasks_with_skip(session, test_tasks):
    skipped_tasks = get_predict_tasks(session, skip=1, limit=2)
    assert len(skipped_tasks) == 2
    assert skipped_tasks[0].id != test_tasks[0].id


def test_get_predict_tasks_empty_result(session):
    tasks = get_predict_tasks(session)
    assert len(tasks) == 0
    assert isinstance(tasks, list)
