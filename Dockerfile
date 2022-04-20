# Feel free to change base image
FROM python:3.8-slim-buster

WORKDIR /src

RUN pip install poetry

COPY requirements.txt .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .
