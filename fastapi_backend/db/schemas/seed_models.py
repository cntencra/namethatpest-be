from pydantic import BaseModel

class InsectDB(BaseModel):
    insect_id: int
    generic_name: str
    specific_name: str

class DevAnimalDB(BaseModel):
    animal_id: int
    generic_name: str
    specific_name: str

class ImgUrlDB(BaseModel):
    image_url: str
    image_attribution: str | None = None
    insect_id: int | None = None
    animal_id: int | None = None

class SeedData(BaseModel):
    insects: list[InsectDB]
    img_urls: list[ImgUrlDB]
    dev_animals: list[DevAnimalDB]