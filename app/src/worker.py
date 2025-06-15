import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from opyoid import Module, Injector
from sqlmodel import Session

from app.src.base.model_starter import get_model
from app.src.base.constants import TaskStatus
from app.src.database.database import engine
from app.src.models.predict_task import PredictTask
from app.src.models.quality_prediction import QualityPrediction
from app.src.services.account_service import AccountService
from app.src.services.crud.prediction import create_prediction
from app.src.services.rabbitmq_task_service import (
    start_consuming_tasks,
    PredictTaskPayload,
)
from app.src.services.transaction_service import TransactionService
from app.src.services.crud.predict_task import update_predict_task

# Загрузка переменных окружения из .env файла, если он существует
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def process_predict_task(ch, method, properties, body, session: Session):
    data = PredictTaskPayload.model_validate_json(body) # проверяет по алиасам
    print(f"Received task: {data}")

    account_service = AccountService(TransactionService())
    predict_task = PredictTask(id=data.id, status=TaskStatus.IN_PROGRESS)

    update_predict_task(predict_task, session)

    try:
        model = get_model() #
        filtered_data = json.loads(data.model_dump_json(by_alias=True))#{key: value for key, value in data.model_dump_json(by_alias=True).items() if key in ['fixed_acidity','volatile_acidity','citric_acid','residual_sugar','chlorides','free_sulfur_dioxide','total_sulfur_dioxide','density','pH','sulphates','alcohol']}
        #worker-2     | AttributeError: 'PredictTaskPayload' object has no attribute 'items'
        print("dict aliased is ",filtered_data)
        filtered_data = {key.replace("_"," "): value for key, value in filtered_data.items() if key in ['fixed_acidity','volatile_acidity','citric_acid','residual_sugar','chlorides','free_sulfur_dioxide','total_sulfur_dioxide','density','pH','sulphates','alcohol']}
        # надо менять нейминги при подстановке
        # todo заменить на подjson
        result = model.predict_result(filtered_data)

        #account_service.create_payment(data.user_id, session) # predict сразу с оплатой - была двойная!

        prediction = QualityPrediction(
            user_id=data.user_id,
            fixed_acidity=data.fixed_acidity,
            volatile_acidity=data.volatile_acidity,
            citric_acid=data.citric_acid,
            residual_sugar=data.residual_sugar,
            chlorides=data.chlorides,
            free_sulfur_dioxide=data.free_sulfur_dioxide,
            total_sulfur_dioxide=data.total_sulfur_dioxide,
            density=data.density,
            pH=data.pH,
            sulphates=data.sulphates,
            alcohol=data.alcohol,
            predicted_quality=result,
            created_at=datetime.now(timezone.utc)
        )

        prediction = create_prediction(prediction, session)

        # upd task
        predict_task.status = TaskStatus.COMPLETED
        predict_task.predicted_quality = prediction.predicted_quality
        update_predict_task(predict_task, session)
    except Exception:
        predict_task.predicted_quality = "Ошибка выполнения. Кредиты будут возвращены"
        predict_task.status = TaskStatus.FAILED
        update_predict_task(predict_task, session)
        account_service.cancel_payment(data.user_id, session)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Predict task id: {predict_task.id} processed")


class Worker:
    def __init__(self, session: Session):
        self.session = session

    def start(self):
        start_consuming_tasks(process_predict_task, self.session)


class WorkerModule(Module):
    def configure(self) -> None:
        self.bind(Session, to_instance=Session(engine))
        self.bind(Worker)


if __name__ == "__main__":
    injector = Injector(modules=[WorkerModule()])
    worker = injector.inject(Worker)
    worker.start()
