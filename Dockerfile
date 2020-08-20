FROM python:3

WORKDIR /project

COPY ./ ./

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
CMD alembic upgrade head && scrapy crawl tesco
