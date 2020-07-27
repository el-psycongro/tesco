FROM python:3

ENV PYTHONIOENCODING=UTF-8

COPY Pipfile.lock ./
COPY Pipfile ./

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

WORKDIR /project
