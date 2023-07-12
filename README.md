# Split building limits API

API that consumes building limits and height plateaus, splits up the building limits
according to the height plateaus, and stores these three entities (building limits,
height plateaus and split building limits) in a persistent way.

The API is deployed at:
The postgres database instance is deployed at: <https://www.elephantsql.com/>.

## API Spec

## Local development

### Setup

Copy the `.envrc.template` to `.envrc`, and run `direnv allow` or source
the `.envrc` file manually. It should contain the database url `DB_URL`
of a deployed or local database.

### Running the service

#### In docker-compose (mounted volume)

```shell
docker compose up
```

#### Locally

A local or deployed database instance is needed to run the application.

```shell
poetry install
poetry run uvicorn src.app:app --reload --port 4011
```

The API docs can be accessed at: <http://127.0.0.1:4011/docs>

## Local testing

Tests are using flask api test client, so there is no need to run the
service.

Make sure you have the `DB_URL` environment variable set.

Run tests with:

```shell
poetry run pytest
```

## Run the examples

The examples can be found in this [jupyter
notebook](examples/split_building_limits_examples.ipynb)

Make sure you have the `DB_URL` environment variable set and the
application running.

To open the examples notebook you can use: `poetry run jupyter
notebook`.

### Requirements

- The `notebook` package. It is part of the dev group dependencies
 so it will automatically be installed using `poetry install`.

## Assumptions

- Height plateaus should fully cover building limits. Otherwise a 400
  (BAD REQUEST) is sent to the client.
- Neither height plateaus or building limits can not contain
  overlapping geometries. Otherwise a 400 (BAD REQUEST) is sent to
  the client.
