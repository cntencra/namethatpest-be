from typing import List
from fastapi import HTTPException
from fastapi_backend.app.models.insect_models import InsectModel
from fastapi_backend.app.schemas.database import Insect

class InsectController:
    def __init__(self) -> None:
        self.insect_model = InsectModel()
   
    async def get_insects(self) -> List[Insect]:
        insects  = await self.insect_model.fetch_insects()
        if len(insects) == 0:
            raise HTTPException(status_code=404, detail=f"No insects found")
        return insects
    