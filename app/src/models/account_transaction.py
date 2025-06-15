from __future__ import annotations
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from app.src.base.constants import TransactionType
from app.src.models.account import Account


class AccountTransaction(SQLModel, table=True):
    __tablename__ = "account_transactions"

    id: int = Field(primary_key=True, default=None)
    type: TransactionType = Field(default=None)
    amount: int
    account_id: int = Field(foreign_key="accounts.id")
    created_at: datetime
    account: Account = Relationship(back_populates="transactions")
