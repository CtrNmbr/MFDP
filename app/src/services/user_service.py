import hashlib
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlmodel import Session, select
from app.src.base.constants import UserRole
from app.src.models.user import User
from app.src.base.config import import_settings
from jose import jwt, JWTError

TOKEN_EXPIRE_TIME_MINUTES = 30 * 60
HASHALG = "HS256"

def hash_password(passw):
    return hashlib.sha256(passw.encode()).hexdigest()

class UserService:

    @staticmethod
    def check_credentials(passw: str, curr_passw) -> bool:
        return hash_password(passw) == curr_passw

    def make_user(self, email: str,
                    passw: str,
                    session: Session,
                    role: UserRole = UserRole.USER):

        if self.get_user_by_email(email, session):
            return {"message": "User exists", "status": False}
        else:
            user = User(email=email,
                        password_hash=hash_password(passw),
                        role=role,
                        last_update_datetime=datetime.now(timezone.utc)
                        )
            session.add(user)
            session.commit()
            return user

    @staticmethod
    def get_user_by_id(id: int, session: Session) -> User:
        user = session.exec(select(User).where(User.id == id)).first()
        return user

    @staticmethod
    def get_user_by_email(email: str, session: Session) -> User:
        user = session.exec(select(User).where(User.email == email)).first()
        return user

    @staticmethod
    def create_token(info: dict, delta: Optional[timedelta] = None):
        payload = info.copy()
        expire = datetime.now(timezone.utc) + (
            delta
            if delta
            else timedelta(minutes=TOKEN_EXPIRE_TIME_MINUTES)
        )
        payload.update({"exp": expire})
        token = jwt.encode(payload, import_settings().JWT_SECRET_KEY, algorithm=HASHALG)
        return token

    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, import_settings().JWT_SECRET_KEY,
                algorithms=[HASHALG],
                options={"verify_sub": False, "verify_jti": False,
                         "verify_aud": False, "verify_iat": False,
                         "verify_nbf": False, "verify_iss": False}
            )
            user_id: int = payload.get("subscriber")
            return user_id
        except JWTError as e:
            print(e)
            return None