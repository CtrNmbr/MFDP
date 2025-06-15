import json
from functools import partial
from typing import Callable

import pika
from sqlmodel import Session

from app.src.dto.predict_task_payload import PredictTaskPayload
from app.src.models.predict_task import PredictTask
from app.src.base.config import import_settings

QUEUE_NAME = "predict_tasks"


def get_rabbitmq_connection():
    settings = import_settings()

    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
    )
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials,
        )
    )


def send_task_to_queue(task: PredictTask):

    with get_rabbitmq_connection() as connection:
        channel = connection.channel()
        channel.queue_declare(QUEUE_NAME, durable=True)

        payload = PredictTaskPayload(
            id=task.id,
            user_id=task.user_id,
            fixed_acidity=task.fixed_acidity,
            volatile_acidity=task.volatile_acidity,
            citric_acid=task.citric_acid,
            residual_sugar=task.residual_sugar,
            chlorides=task.chlorides,
            free_sulfur_dioxide=task.free_sulfur_dioxide,
            total_sulfur_dioxide=task.total_sulfur_dioxide,
            density=task.density,
            pH=task.pH,
            sulphates=task.sulphates,
            alcohol=task.alcohol,
            account_transaction_id=task.account_transaction_id,
        )

        message = payload.model_dump_json()

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )


def start_consuming_tasks(task_processor: Callable, session: Session):
    with get_rabbitmq_connection() as connection:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=partial(task_processor, session=session),
        )

        print("Consuming started. Waiting for tasks...")
        channel.start_consuming()
