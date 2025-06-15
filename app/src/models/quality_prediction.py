from datetime import datetime

from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING

#from app.src.models.user import User #ImportError: cannot import name 'User' from partially initialized module 'app.src.models.user' (most likely due to a circular import) (D:\Karpov courses\HW\4MLSERVICE\5MLServiceInteraction\ml_service_python\app\src\models\user.py)
#if TYPE_CHECKING:

from app.src.models.user import User

class QualityPrediction(SQLModel, table=True):
    __tablename__ = "predictions"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
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
    predicted_quality: float = Field()
    created_at: datetime = Field()
    user: User = Relationship(back_populates="predictions")
