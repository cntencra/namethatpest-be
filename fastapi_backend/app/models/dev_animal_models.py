from typing import List
from fastapi_backend.db.db_manager import db_manager
from fastapi_backend.app.schemas.database import DevAnimal

class DevAnimalModel():
             
    @staticmethod
    async def fetch_dev_animals() -> List[DevAnimal]:
        async with db_manager.get_conn() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT dev_animals.animal_id, dev_animals.generic_name, dev_animals.specific_name, img_urls.image_url, img_urls.image_attribution  FROM dev_animals JOIN img_urls ON dev_animals.animal_id = img_urls.animal_id")
                rows = await cur.fetchall()
                return [
                    DevAnimal(
                        animal_id=row[0],
                        generic_name=row[1],
                        specific_name=row[2],
                        image_url=row[3],
                        image_attribution=row[4]
                    ) for row in rows
                ]