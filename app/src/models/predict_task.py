import uuid
from typing import Optional
from app.src.base.constants import TaskStatus
from sqlmodel import SQLModel, Field

class PredictTask(SQLModel, table=True):
    __tablename__ = "predict_tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    #TODO передавать по сети json - грузить их анбоксинг
    fixed_acidity: float = Field(alias='fixed acidity')
    volatile_acidity: float = Field(alias='volatile acidity')
    citric_acid: float = Field(alias='citric acid')
    residual_sugar: float = Field(alias='residual sugar')
    chlorides: float = Field()
    free_sulfur_dioxide: float = Field(alias='free sulfur dioxide')
    total_sulfur_dioxide: float = Field(alias='total sulfur dioxide')
    density: float = Field()
    pH: float = Field()
    sulphates: float = Field()
    alcohol: float = Field()
    predicted_quality: Optional[float] = Field()
    #result: Optional[float]
    status: TaskStatus = Field(default=TaskStatus.CREATED)
    account_transaction_id: int = Field(
        foreign_key="account_transactions.id", nullable=False
    )