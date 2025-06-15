import uuid
from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlmodel import select, Session
from app.src.models.predict_task import PredictTask
from app.src.base.constants import TaskStatus


def create_predict_task(predict_task: PredictTask, session: Session) -> PredictTask:
    session.add(predict_task)
    session.commit()
    session.refresh(predict_task)
    return predict_task


def update_predict_task(updated_task: PredictTask, session: Session) -> PredictTask:
    existing_task = get_predict_task(updated_task.id, session)

    existing_task.predicted_quality = updated_task.predicted_quality if updated_task.predicted_quality else None
    existing_task.status = updated_task.status

    session.commit()
    session.refresh(existing_task)
    return existing_task


def get_predict_task(task_id: uuid.UUID, session: Session) -> PredictTask:
    try:
        statement = select(PredictTask).where(PredictTask.id == task_id)
        prediction = session.exec(statement).one()
        return prediction
    except NoResultFound:
        raise ValueError(f"PredictTask with id {task_id} not found")


def delete_predict_task(task_id: uuid.UUID, session: Session) -> None:
    task = get_predict_task(task_id, session)
    session.delete(task)
    session.commit()


def get_predict_tasks(
    session: Session,
    user_id: Optional[int] = None,
    status: Optional[TaskStatus] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[PredictTask]:
    query = select(PredictTask)

    if user_id:
        query = query.where(PredictTask.user_id == user_id)
    if status:
        query = query.where(PredictTask.status == status)
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()
