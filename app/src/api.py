from app.src.routes.account import account_router
from app.src.routes.ml_model import ml_model_router
from app.src.routes.user import user_route
from app.src.database.database import init_db

from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

import uvicorn

#env_path = Path(__file__).parent.parent / ".env"
#if env_path.exists():
#    print('env exists')
#    load_dotenv(env_path)

@asynccontextmanager
async def at_start(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=at_start)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_origins=["*"]
)

app.include_router(account_router, prefix="/account")
app.include_router(ml_model_router, prefix="/model")
app.include_router(user_route, prefix="/user")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
