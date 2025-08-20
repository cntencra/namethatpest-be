from pydantic import BaseModel

class Insect(BaseModel):
    insect_id: int
    generic_name: str
    specific_name: str
    image_url: str
    image_attribution: str | None = None

class DevAnimal(BaseModel):
    animal_id: int
    generic_name: str
    specific_name: str
    image_url: str
    image_attribution: str | None = None