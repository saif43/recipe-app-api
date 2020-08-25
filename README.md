# recipe-app-api

## Create Dockerfile

```docker
FROM python:3.7-alpine
LABEL maintainer="Saif Ahmed Anik"


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
```

Now run

```bash
docker build .
```

---

## Create docker-compose.yml

```docker
version: "3"

services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
```

Now run

```bash
docker-compose build
```

---

## Create Django Project

Run

```bash
docker-compose run app sh -c "django-admin.py startproject app ."
```

---

## Create core app

Run

```bash
docker-compose run app sh -c "python manage.py startapp core"
```

---

## Add Postgres to docker-compose

Run

```docker
version: "3"

services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
    environment:
      - DB_HOST=db
      - DB_NAME=app
      - DB_USER=postgres
      - DB_PASS=supersecretpassword
    depends_on:
      - db

  db:
    image: postgres:10-alpine
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=supersecretpassword

```

---

## Add Postgres support to Docker file

```docker
FROM python:3.7-alpine
LABEL maintainer="Saif Ahmed Anik"


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
```
