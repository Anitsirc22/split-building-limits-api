FROM python:3.10-slim


RUN apt-get update && apt-get -y upgrade && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# psycopg needs libpq-dev
# RUN apt-get install -y libpq-dev
RUN pip install poetry

RUN mkdir /src
# WORKDIR /src

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry add psycopg-binary
RUN poetry install --only main

COPY /src /src

CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5001"]
