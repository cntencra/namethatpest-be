from typing import List
from fastapi_backend.db.db_manager import db_manager
from fastapi_backend.app.schemas.database import Insect

class InsectModel():
             
    @staticmethod
    async def fetch_insects() -> List[Insect]:
        async with db_manager.get_conn() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT insects.insect_id, insects.generic_name, insects.specific_name, img_urls.image_url, img_urls.image_attribution  FROM insects JOIN img_urls ON insects.insect_id = img_urls.insect_id")
                rows = await cur.fetchall()
                return [
                    Insect(
                        insect_id=row[0],
                        generic_name=row[1],
                        specific_name=row[2],
                        image_url=row[3],
                        image_attribution=row[4]
                    ) for row in rows
                ]