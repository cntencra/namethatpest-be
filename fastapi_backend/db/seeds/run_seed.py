from fastapi_backend.db.db_manager import db_manager
from fastapi_backend.db.utils.seed_utils import load_seed_data
from fastapi_backend.db.seeds.seed import seed
from fastapi_backend.utils.path_utils import get_project_root
import os

async def run_seed():
    dev_data_path = get_project_root() / "fastapi_backend" / "db" / "data" / "dev_data" / "seed_data.json"
    os.environ["ENV"] = "dev"
    await db_manager.init_env()
    await db_manager.open_pool()
    print("🔗 Database connection pool opened.")
    seed_data = load_seed_data(dev_data_path)
    await seed(db_manager, seed_data)
    print("✅ Dev Database seeded.")

    await db_manager.close_pool()
    print("🧹 Pool closed.")

def main():
    import asyncio
    asyncio.run(run_seed())

if __name__ == "__main__":
    main()