from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.src.database.database import get_session
from app.src.dto.account_fund_request import AccountFundRequest
from app.src.services.account_service import AccountService
from app.src.services.transaction_service import TransactionService
from app.src.services.user_service import UserService
from app.src.dto.account_details import AccountDetails, TransactionDetails

account_router = APIRouter(tags=["Account"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #OAuth2PasswordBearer(tokenUrl="/user/signin") # OAuth2PasswordBearer(tokenUrl="token")


@account_router.get("/details", response_model=AccountDetails)
def get_account_details(
    token: str = Depends(oauth2_scheme), session=Depends(get_session)
):
    user_id = UserService.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    account_service = AccountService(TransactionService())
    account_details = account_service.get_account_with_transactions(
        user_id, session=session
    )

    return AccountDetails(
        balance=account_details.balance,
        user_id=user_id,
        transactions=[
            TransactionDetails(
                id=tx.id,
                type=tx.type,
                amount=tx.amount,
                account_id=tx.account_id,
                created_at=tx.created_at,
            )
            for tx in account_details.transactions
        ],
    )


@account_router.post("/fund")
def add_funds(
    request: AccountFundRequest,
    token: str = Depends(oauth2_scheme),
    session=Depends(get_session),
):
    user_id = UserService.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    if request.amount < 0:
        raise HTTPException(
            status_code=400, detail="Сумма пополнения не может быть отрицательной"
        )

    account_service = AccountService(TransactionService())
    account_service.fund(user_id, request.amount, session=session)
