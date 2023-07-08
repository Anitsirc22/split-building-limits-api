# Split building limits API

API that consumes building limits and height plateaus, splits up the building limits
according to the height plateaus,and stores these three entities (building limits,
height plateaus and split building limits) in a persistent way.

## Local development

### Setup

Copy the `.envrc.template` to `.envrc`, and run `direnv allow` or source the `.envrc`
file manually

### Running the service

#### In docker-compose (mounted volume)

#### Locally

```shell
poetry install
poetry run uvicorn src.app:app --reload --port 4011
<!-- poetry run python src/app.py -->
```

## Local testing

Tests are using flask api test client, so there is no need to run the service.

```shell
poetry run pytest
```
