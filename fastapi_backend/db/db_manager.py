import os
from dotenv import load_dotenv
from psycopg import AsyncConnection 
from psycopg_pool import AsyncConnectionPool
from typing import AsyncGenerator
from contextlib import asynccontextmanager

class _DBManager:

    def __init__ (self):
        if hasattr(self, "_initialized") and self._initialized:
            return 
        
        self._initialized = True
        self._env_selected = False
        self._async_pool: AsyncConnectionPool | None = None
        self._database_url: str | None = None
        self._env_mode: str = "dev"
    
    async def init_env(self):
        if self._env_selected:
            return 
        
        self._env_selected = True

        self._env_mode = os.getenv("ENV", "dev")
        env_file= f".env.{self._env_mode}"

        load_dotenv(env_file)

        self._database_url = os.getenv("DATABASE_URL")
        if not self._database_url:
            pg_db = os.getenv("PGDATABASE")
            pg_user = os.getenv("PGUSER")
            pg_password = os.getenv("PGPASSWORD")
            pg_host = os.getenv("PGHOST", "localhost")
            pg_port = int(os.getenv("PGPORT", 5432))

            if not all([pg_db, pg_user, pg_password]):
                raise RuntimeError(
                    "Missing database configuration! "
                    "Set DATABASE_URL or PGDATABASE/PGUSER/PGPASSWORD."
                )

            self._database_url = (
                f"postgresql+psycopg://{pg_user}:{pg_password}"
                f"@{pg_host}:{pg_port}/{pg_db}"
            )

        print(f"\n🔗 Using database for {self._env_mode.capitalize()}")


    async def open_pool(self):
        if not self._env_selected:
            raise RuntimeError("Environment not initialized. Call init_env() first.")
        
        if self._async_pool is None:
            self._async_pool = AsyncConnectionPool(open=False)
            print(f"🔗 {self._env_mode.capitalize()} Database connection pool opened.")
            await self._async_pool.open()

    async def close_pool(self):
        if self._async_pool is not None:
            await self._async_pool.close()
            print(f"\n🧹 {self._env_mode.capitalize()} Database connection pool closed.")
            self._async_pool = None

    @asynccontextmanager
    async def get_conn(self) -> AsyncGenerator[AsyncConnection, None]:
        if self._async_pool is None:
            raise RuntimeError("Database pool has not been initialized")
        async with self._async_pool.connection() as conn:
            yield conn

db_manager = _DBManager()