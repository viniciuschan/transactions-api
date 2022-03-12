FROM python:3.10.2

RUN pip3 install --no-cache --upgrade pip setuptools && pip3 install poetry

ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL postgres://postgres:supersecret@db:5432/postgres
ENV SECRET_KEY django-insecure-!er9pb#owst_j9leytvf9g#m5j^l&6vgl@zt$e%77w@9938zu1
ENV DEBUG True

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install

COPY . /app/
