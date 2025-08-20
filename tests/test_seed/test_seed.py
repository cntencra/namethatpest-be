import pytest
from fastapi_backend.db.db_manager import _DBManager
from psycopg.rows import dict_row
from psycopg import sql

pytestmark = pytest.mark.anyio

@pytest.mark.parametrize("table_name", [
    "insects",
    "img_urls",
    "dev_animals"
])
async def test_tables_exists(db_manager_fixture: _DBManager, table_name: str):
    async with db_manager_fixture.get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, (table_name,))
      
            exists = await cur.fetchone()
            assert exists is not None, "Query returned no rows"
            assert exists[0], f"Table '{table_name}' does not exist."

@pytest.mark.parametrize("table_name, column_name, data_type", [
    ("insects","insect_id","integer"),
    ("insects","generic_name","character varying"),
    ("insects","specific_name","character varying"),
    ("img_urls","url_id","integer"),
    ("img_urls","image_url","text"),
    ("img_urls","insect_id","integer"),
    ("img_urls","animal_id","integer"),
    ("dev_animals","animal_id","integer"),
    ("dev_animals","generic_name","character varying"),
    ("dev_animals","specific_name","character varying"),

])
async def test_table_column_data_type(db_manager_fixture: _DBManager, table_name: str, column_name: str, data_type:str):
    async with db_manager_fixture.get_conn() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
            SELECT *
            FROM information_schema.columns
            WHERE table_name = %s
            AND column_name = %s
                              
            """, (table_name, column_name))

            result = await cur.fetchone()
            assert result is not None, f"{table_name} or {column_name} does not exist."
            assert result["data_type"] == data_type, f"Column '{column_name}' in table '{table_name}' is not of type {data_type}."

@pytest.mark.parametrize("table_name, columns, test_data_length, nullable_columns",[

    ("img_urls", ["url_id", "image_url", "image_attribution","insect_id", "animal_id",], 10, ["insect_id", "animal_id", "image_attribution"]),
    ("insects", ["insect_id", "generic_name", "specific_name"], 5, []),
    ("dev_animals", ["animal_id", "generic_name", "specific_name"], 5, []),
]
)
async def test_table_data(db_manager_fixture: _DBManager, table_name, columns, test_data_length, nullable_columns):
    async with db_manager_fixture.get_conn() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            await cur.execute(query)
            rows = await cur.fetchall()

            assert rows, f"Table '{table_name}' is empty."
            assert len(rows) == test_data_length, f"Table '{table_name}' does not have the expected number of rows."

            for row in rows:
                for column in columns:
                    assert column in row, f"Column '{column}' is missing in table '{table_name}'."
                    if column not in nullable_columns:
                        assert row[column] is not None, f"Column '{column}' in table '{table_name}' has a NULL value."