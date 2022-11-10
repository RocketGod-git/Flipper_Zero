FROM python:3.7.3-alpine3.9

WORKDIR /usr/src/app

RUN pip install pipenv
RUN set -ex && \
    apk add --no-cache build-base linux-headers

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --dev --ignore-pipfile --system

COPY . .
