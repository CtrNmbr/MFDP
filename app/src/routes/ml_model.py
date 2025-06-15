import json
import uuid
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.src.base.constants import TaskStatus
from app.src.database.database import get_session
from app.src.dto.prediction import Prediction
from app.src.dto.prediction_request import PredictionRequest
from app.src.models.account_transaction import AccountTransaction
from app.src.models.predict_task import PredictTask
from app.src.services.account_service import AccountService
from app.src.services.crud.predict_task import create_predict_task, get_predict_task
from app.src.services.crud.prediction import get_predictions
from app.src.services.rabbitmq_task_service import send_task_to_queue
from app.src.services.transaction_service import TransactionService
from app.src.services.user_service import UserService

ml_model_router = APIRouter(tags=["ML Model"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #OAuth2PasswordBearer(tokenUrl="/user/signin") #OAuth2PasswordBearer(tokenUrl="token")


@ml_model_router.post("/predict")
def predict(
    predication_request: PredictionRequest,
    token: str = Depends(oauth2_scheme),
    session=Depends(get_session),
):
    """Анализ качества вина"""

    user_id = UserService.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    account_service = AccountService(TransactionService())

    transaction_result = account_service.create_payment(
        user_id, session
    )
    if not isinstance(transaction_result, AccountTransaction):
        return transaction_result

    # create task
    predict_task = PredictTask(
        user_id=user_id,
        status=TaskStatus.CREATED,
        fixed_acidity= predication_request.fixed_acidity,
        volatile_acidity= predication_request.volatile_acidity,
        citric_acid= predication_request.citric_acid,
        residual_sugar= predication_request.residual_sugar,
        chlorides= predication_request.chlorides,
        free_sulfur_dioxide= predication_request.free_sulfur_dioxide,
        total_sulfur_dioxide= predication_request.total_sulfur_dioxide,
        density= predication_request.density,
        pH= predication_request.pH,
        sulphates= predication_request.sulphates,
        alcohol= predication_request.alcohol,
        account_transaction_id=transaction_result.id,
    )
    predict_task = create_predict_task(predict_task, session)

    send_task_to_queue(predict_task)

    return {
        "task_id": predict_task.id,
    }


@ml_model_router.get("/predictResult/{task_id}")
def get_task(
    task_id: uuid.UUID,
    token: str = Depends(oauth2_scheme),
    session=Depends(get_session),
):
    """Анализ качества вина"""

    user_id = UserService.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    task = get_predict_task(task_id, session)
    return {
        "id": task.id,
        "status": task.status,
        "fixed_acidity":task.fixed_acidity,
        "volatile_acidity":task.volatile_acidity,
        "citric_acid":task.citric_acid,
        "residual_sugar":task.residual_sugar,
        "chlorides":task.chlorides,
        "free_sulfur_dioxide":task.free_sulfur_dioxide,
        "total_sulfur_dioxide":task.total_sulfur_dioxide,
        "density":task.density,
        "pH":task.pH,
        "sulphates":task.sulphates,
        "alcohol":task.alcohol,
        "predicted_quality": task.predicted_quality if task.predicted_quality is not None else None,
    }


@ml_model_router.get("/history")
def get_prediction_history(
    token: str = Depends(oauth2_scheme), session=Depends(get_session)
) -> List[Prediction]:
    """Просмотр истории запросов на предсказания."""

    user_id = UserService.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    predictions = get_predictions(user_id, session)
    return [
        Prediction(
            id=p.id,
            fixed_acidity=p.fixed_acidity,
            volatile_acidity=p.volatile_acidity,
            citric_acid=p.citric_acid,
            residual_sugar=p.residual_sugar,
            chlorides=p.chlorides,
            free_sulfur_dioxide=p.free_sulfur_dioxide,
            total_sulfur_dioxide=p.total_sulfur_dioxide,
            density=p.density,
            pH=p.pH,
            sulphates=p.sulphates,
            alcohol=p.alcohol,
            predicted_quality=p.predicted_quality,
            created_at=p.created_at,
        )
        for p in predictions
    ]
