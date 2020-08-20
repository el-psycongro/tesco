from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(get_project_settings().get("DB_URL"))

Base = declarative_base()
