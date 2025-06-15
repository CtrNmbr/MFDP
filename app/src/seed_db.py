from sqlmodel import Session

from app.src.base.constants import UserRole
from app.src.services.account_service import AccountService
from app.src.services.transaction_service import TransactionService
from app.src.services.user_service import UserService


def seed_db(session: Session):
    user_service = UserService()
    account_service = AccountService(TransactionService())

    demo_user = user_service.make_user("demo@email.com", "Pass123", session)
    user_service.make_user("admin@email.com", "Pass123", session, UserRole.ADMIN)

    account_service.create_account(demo_user.id, session)
    account_service.fund(demo_user.id, 50, session)
    account_service.refund(demo_user.id, 5, session)
    account_service.create_payment(demo_user.id, session)
    account_service.get_account_with_transactions(user_id=demo_user.id, session=session)
