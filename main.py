from fastapi import FastAPI
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

app.include_router(api.router, prefix="/api")