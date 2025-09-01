from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi_backend.db.db_manager import db_manager
from fastapi_backend.app.routes import api


@asynccontextmanager
async def lifespan(app: FastAPI):

    await db_manager.init_env()
  
    await db_manager.open_pool()
    
    yield
  
    await db_manager.close_pool()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://192.168.0.14:3000",
    "https://namethatpest.co.uk",
    "https://www.namethatpest.co.uk",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")