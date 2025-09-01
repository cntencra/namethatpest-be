
# fastapi-backend
This is the backend for my insect test visualisation
Written using FastAPI and poetry for environment and version control

## Clone the repo
```bash
cd ~/path_to_dir/

git clone https://github.com/cntencra/namthatpest-be
``` 
## Install uv, 
[uv install](https://docs.astral.sh/uv/getting-started/installation/)

## Set up the .env.* files
```
.env.dev
    PGDATABASE = insect_test
    PGHOST=localhost
    

.env.test
    PGDATABASE = insect_test_test
    PGHOST=localhost
```

## Seed local dev database
```bash
psql -f fastapi_backend/db/setup-dbs.sql

uv run fastapi_backend/db/seeds/run_seed.py
```


```bash
uv run fastapi_backend/db/seeds/run_seed
```


## run tests
```bash
uv run pytest -s tests
```

-s flag shows print output



## run dev server
```bash

uv run fastapi dev main.py
```

## run prod server
```
ENV= production uv run fastapi run main.py
```
