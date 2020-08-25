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
