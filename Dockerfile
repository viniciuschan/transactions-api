FROM python:3.10.2

ENV PYTHONUNBUFFERED 1

ENV DATABASE_URL postgres://postgres:supersecret@db:5432/postgres
ENV SECRET_KEY django-insecure-!er9pb#owst_j9leytvf9g#m5j^l&6vgl@zt$e%77w@9938zu1
ENV DEBUG True

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry export -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt

COPY . /app/
