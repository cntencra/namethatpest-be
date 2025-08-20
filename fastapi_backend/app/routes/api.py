from fastapi import APIRouter
from fastapi_backend.app.controllers.insect_controllers import InsectController
from fastapi_backend.app.controllers.dev_animal_controllers import DevAnimalController
from fastapi_backend.app.schemas.database import Insect, DevAnimal

router = APIRouter()

insect_controller = InsectController()
dev_animal_controller = DevAnimalController()

@router.get("/insects", response_model=list[Insect])   
async def get_insects():
    return await insect_controller.get_insects()

@router.get("/dev_animals", response_model=list[DevAnimal])
async def get_dev_animals():
    return await dev_animal_controller.get_dev_animals()