import os
import pytest
from typing import AsyncGenerator

from fastapi_backend.db.db_manager import db_manager, _DBManager
from fastapi_backend.utils.path_utils import get_project_root
from fastapi_backend.db.utils.seed_utils import load_seed_data
from fastapi_backend.db.seeds.seed import seed

# database seeding fixture
# This fixture will be used to seed the database with test data before running tests.

@pytest.fixture(scope="module")
async def db_manager_fixture() -> AsyncGenerator[_DBManager, None]: 
    test_data_path = get_project_root() / "fastapi_backend" / "db" / "data" / "test_data" / "seed_data.json"
    os.environ["ENV"] = "test"
    await db_manager.init_env()
    await db_manager.open_pool()
    seed_data = load_seed_data(test_data_path)
    await seed(db_manager, seed_data)
    print(f"✅ {os.environ['ENV'].capitalize()} Database seeded.")
    yield db_manager
    await db_manager.close_pool()
    
