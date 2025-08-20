from fastapi_backend.db.db_manager import  _DBManager
from fastapi_backend.db.schemas.seed_models import SeedData

async def seed(
        db_manager: _DBManager,
        seed_data: SeedData,
    ):

    async with  db_manager.get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(""" 
                DROP TABLE IF EXISTS img_urls;
                DROP TABLE IF EXISTS dev_animals;
                DROP TABLE IF EXISTS insects;
            """)
            await cur.execute("""
                CREATE TABLE insects
                (
                insect_id SERIAL PRIMARY KEY NOT NULL,
                generic_name VARCHAR(200) NOT NULL,
                specific_name VARCHAR(200) NOT NULL
                )
            """)
            await cur.execute("""
                CREATE TABLE dev_animals
                (
                animal_id SERIAL PRIMARY KEY NOT NULL,
                generic_name VARCHAR(200) NOT NULL,
                specific_name VARCHAR(200) NOT NULL
                )
            """)
            await cur.execute("""
                CREATE TABLE img_urls
                (
                url_id SERIAL PRIMARY KEY NOT NULL,
                image_url TEXT NOT NULL,
                image_attribution TEXT,
                insect_id INTEGER REFERENCES insects(insect_id) ON DELETE CASCADE,
                animal_id INTEGER REFERENCES dev_animals(animal_id) ON DELETE CASCADE
                )
            """)
            await cur.executemany("""
                INSERT INTO insects (insect_id, generic_name, specific_name)
                VALUES (%s, %s, %s)
            """, [(insect.insect_id, insect.generic_name, insect.specific_name) for insect in seed_data.insects])
            await cur.executemany("""
                INSERT INTO dev_animals (animal_id, generic_name, specific_name)
                VALUES (%s, %s, %s)
            """, [(dev_animal.animal_id, dev_animal.generic_name, dev_animal.specific_name) for dev_animal in seed_data.dev_animals])
            await cur.executemany("""
                INSERT INTO img_urls (image_url, image_attribution, insect_id, animal_id)
                VALUES (%s, %s, %s, %s)
            """, [(img_url.image_url, img_url.image_attribution, img_url.insect_id, img_url.animal_id) for img_url in seed_data.img_urls])


            await conn.commit()