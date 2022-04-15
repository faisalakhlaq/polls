# syntax=docker/dockerfile:1
FROM python:3.10-alpine
LABEL authos="Faisal Akhlaq"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apk add --no-cache postgresql postgresql-dev
RUN apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

COPY . /code/
