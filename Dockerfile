FROM python:3.10.2

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry export -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt

COPY . /app/
