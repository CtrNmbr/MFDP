from typing import List
from datetime import datetime
from pydantic import BaseModel
from app.src.base.constants import TransactionType

class TransactionDetails(BaseModel):
    id: int
    type: TransactionType
    amount: int
    account_id: int
    created_at: datetime

class AccountDetails(BaseModel):
    balance: int
    user_id: int
    transactions: List[TransactionDetails]
