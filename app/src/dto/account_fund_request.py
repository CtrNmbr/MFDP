from pydantic import BaseModel

class AccountFundRequest(BaseModel):
    amount: int
