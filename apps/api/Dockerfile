FROM python:3.11.6-slim

RUN apt-get update && \
    apt-get install build-essential -y --no-install-recommends
RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

RUN poetry install --without dev
EXPOSE 9000

ENTRYPOINT ["make", "run"]
