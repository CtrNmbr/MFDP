from sqlmodel import SQLModel, Field, Relationship
from typing import List,TYPE_CHECKING
#from app.src.models.user import User

if TYPE_CHECKING:
    from app.src.models.account_transaction import AccountTransaction

from app.src.models.user import User

class Account(SQLModel, table=True):

    __tablename__ = "accounts"

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="users.id")
    balance: int
    cost_per_object: int
    transactions: List["AccountTransaction"] = Relationship(back_populates="account")
    user: User = Relationship(back_populates="account")

    def change_balance(self, amount_w_sign: int):
        self.balance = self.balance + amount_w_sign
