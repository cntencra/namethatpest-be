from typing import List
from fastapi import HTTPException
from fastapi_backend.app.models.dev_animal_models import DevAnimalModel
from fastapi_backend.app.schemas.database import DevAnimal

class DevAnimalController:
    def __init__(self) -> None:
        self.dev_animal_model = DevAnimalModel()
   
    async def get_dev_animals(self) -> List[DevAnimal]:
        dev_animals  = await self.dev_animal_model.fetch_dev_animals()
        if len(dev_animals) == 0:
            raise HTTPException(status_code=404, detail=f"No dev animals found")
        return dev_animals
    