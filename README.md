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

Make sure you have the `DB_URL` environment variable set.

Run tests with:

```shell
poetry run pytest
```

## Build image

```shell
docker build -t split_building_limits .
```

<!-- docker run -it split_building_limits /bin/bash -->

<!-- docker run -it -p 5000:5000 split_building_limits /bin/bash -->

## Run the examples

The examples can be found in this [jupyter notebook](examples/split_building_limits_examples.ipynb)

Make sure you have the `DB_URL` environment variable set.

To run the examples you can use: `poetry run jupyter notebook`.

### Requirements

- The `notebook` package. It is part of the dev group dependencies so it will
automatically be installed using `poetry install`.
