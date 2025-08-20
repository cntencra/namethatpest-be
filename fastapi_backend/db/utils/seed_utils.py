import json
from pathlib import Path
from fastapi_backend.db.schemas.seed_models import SeedData

def load_seed_data(filepath :Path) -> SeedData :
    with open(filepath) as f:
        data = json.load(f)

    return SeedData(**data)
