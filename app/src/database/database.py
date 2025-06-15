from sqlmodel import SQLModel, Session, create_engine
from app.src.base.config import import_settings, Settings

def DATABASE_URL_asyncpg(settings: Settings):
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

def DATABASE_URL_psycopg(settings: Settings):
    return (
        f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASS}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

engine = create_engine(
    url=DATABASE_URL_psycopg(import_settings()), echo=False, pool_size=5, max_overflow=10
)

def get_session() -> Session:  # type: ignore
    with Session(engine) as session:
        yield session

def init_db():
    from sqlalchemy_utils import database_exists, create_database

    # Создаем базу данных, если её нет
    if not database_exists(engine.url):
        create_database(engine.url)
        print("DB was created")

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
