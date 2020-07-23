# -*- coding: utf-8 -*-

import os
import logging
from os.path import dirname
from dotenv import load_dotenv

BOT_NAME = 'tesco'

SPIDER_MODULES = ['tesco.spiders']
NEWSPIDER_MODULE = 'tesco.spiders'

ROBOTSTXT_OBEY = False

# ***  LOGGER  ***
TOP_DIR = dirname(dirname(os.path.abspath(__file__)))
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(TOP_DIR, BOT_NAME + '_logger.log')
logger = logging.getLogger(__name__)


# *** DATABASE ***
load_dotenv(os.path.join(TOP_DIR, '.env'))
CONNECTION_STRING = os.getenv("DB_URL")

ITEM_PIPELINES = {
     'tesco.pipelines.defaultitemvalue.DefaultItemValuePipeline': 200,
     'tesco.pipelines.product.ProductPipeline': 300,
     'tesco.pipelines.usuallyboughtnext.UsuallyBoughtNextPipeline': 400,
     'tesco.pipelines.review.ReviewPipeline': 500,
}

