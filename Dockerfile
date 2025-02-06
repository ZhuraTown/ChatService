FROM python:3.12.2-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    git \
    musl-dev \
    libc-dev \
    libffi-dev \
    build-base


COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip poetry==1.8.5 wheel \
    && poetry config virtualenvs.create false \
    && poetry install --only main

COPY ./src /src

WORKDIR ./src

RUN chmod +x entrypoint.sh
