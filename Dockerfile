FROM python:3.11-slim-bookworm as build


RUN apt-get update && apt-get -y upgrade && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# RUN apt-get build-essential && apt-get install -y libpq-dev
RUN apt-get update && apt-get install -y build-essential libpq-dev

RUN pip install poetry
RUN mkdir /src

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
# RUN poetry add psycopg-binary
RUN poetry install --only main


FROM python:3.11-slim-bookworm
COPY --from=build /usr/local/lib/python3.11/ /usr/local/lib/python3.11/
COPY --from=build /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY /src /src

CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5001"]
