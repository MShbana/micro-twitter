FROM python:3.10.15-alpine3.20

LABEL maintainer="MShbana@protonmail.ch"

ARG DEV=false
WORKDIR /backend
ENV PYTHONUNBUFFERED 1

RUN apk update --no-cache && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        python3-dev \
        zlib \
        zlib-dev \
        linux-headers \
        musl-locales \
        musl-locales-lang \
    && apk add --no-cache \
        postgresql-dev \
        gettext \
        jpeg-dev


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [[ "${DEV}" = "true" ]]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \ 
    rm -rf /tmp

RUN apk del .build-deps

RUN adduser \
        --disabled-password \
        --no-create-home \
        nonroot_user

USER nonroot_user

COPY . .

ENV PATH="/py/bin:$PATH"

EXPOSE 8000
