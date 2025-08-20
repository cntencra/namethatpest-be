import pytest
import os
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from main import app
from fastapi import FastAPI

from fastapi_backend.db.db_manager import db_manager
from fastapi_backend.db.utils.seed_utils import load_seed_data
from fastapi_backend.db.seeds.seed import seed
from fastapi_backend.utils.path_utils import get_project_root

# This fixture provides an instance of the FastAPI application for testing.
# It uses the LifespanManager to manage the application lifespan during tests.
# The `test_app` fixture is scoped to the session, meaning it will be created once per test session.

@pytest.fixture(scope="module", autouse=True)
async def seed_test_db() : 
    test_data_path = get_project_root() / "fastapi_backend" / "db" / "data" / "test_data" / "seed_data.json"
    os.environ["ENV"] = "test"
    await db_manager.init_env()
    await db_manager.open_pool()
    seed_data = load_seed_data(test_data_path)
    await seed(db_manager, seed_data)
    print(f"✅ {os.environ['ENV'].capitalize()} Database seeded.")
    await db_manager.close_pool()
    

@pytest.fixture(scope="module")
async def test_app() -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="module")
async def async_client(test_app : FastAPI) -> AsyncGenerator[AsyncClient, None]:    
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test/api") as client:
        print("🔗 AsyncClient created for testing.")
        yield client