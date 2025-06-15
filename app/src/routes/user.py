from fastapi import APIRouter, HTTPException, status, Depends
from app.src.database.database import get_session

from app.src.dto.user import User
from app.src.services.account_service import AccountService
from app.src.services.transaction_service import TransactionService
from app.src.services.user_service import UserService

user_route = APIRouter(tags=["User"])


@user_route.post("/signup")
async def signup(user: User, session=Depends(get_session)) -> dict:
    if UserService.get_user_by_email(user.email, session) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists",
        )

    user_service = UserService()
    created_user = user_service.make_user(user.email, user.password, session)

    account_service = AccountService(TransactionService())
    account_service.create_account(created_user.id, session)

    return {"message": "User successfully registered!"}


@user_route.post("/signin")
async def signin(user: User, session=Depends(get_session)) -> dict:
    existing_user = UserService.get_user_by_email(user.email, session)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    creds_valid = UserService.check_credentials(
        user.password, existing_user.password_hash
    )
    if not creds_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    claims = {
        "subscriber": existing_user.id,
        "user_role": existing_user.role,
    }
    access_token = UserService.create_token(info=claims)
    return {"access_token": access_token, "token_type": "bearer"}
