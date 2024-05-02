FROM python:3.11-alpine
LABEL authors="Dmitriy Panin"

RUN pip install poetry
WORKDIR /botfarm

COPY . .
RUN poetry install

CMD poetry run pytest && poetry run alembic upgrade head && poetry run python main.py
