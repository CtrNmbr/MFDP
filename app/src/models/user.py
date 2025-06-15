from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from app.src.base.constants import UserRole
#from app.src.models.quality_prediction import QualityPrediction

# такая добавка ппомогла разрешить круговые импорты
if TYPE_CHECKING:
    from app.src.models.account import Account
    from app.src.models.quality_prediction import QualityPrediction

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, default=None)
    email: str = Field(unique=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.USER)
    last_update_datetime: datetime
    account: Optional["Account"] = Relationship(back_populates="user")
    predictions: List["QualityPrediction"] = Relationship(back_populates="user")
