# -*- coding: utf-8 -*-

import os
import logging
import time

BOT_NAME = 'tesco'

SPIDER_MODULES = ['tesco.spiders']
NEWSPIDER_MODULE = 'tesco.spiders'

ROBOTSTXT_OBEY = False

# ***  LOGGER  ***
LOG_LEVEL = "INFO"
LOG_FILE = BOT_NAME + str(int(time.time())) + '.log'
logger = logging.getLogger(__name__)

# *** DATABASE ***
DB_URL = os.getenv("DB_URL")

ITEM_PIPELINES = {
    'tesco.pipelines.defaultitemvalue.DefaultItemValuePipeline': 200,
    'tesco.pipelines.product.ProductPipeline': 300,
    'tesco.pipelines.usuallyboughtnext.UsuallyBoughtNextPipeline': 400,
    'tesco.pipelines.review.ReviewPipeline': 500,
}

# SPIDER_MIDDLEWARES = {
#    'tesco.middlewares.middlewares.TescoSpiderMiddleware': 543,
# }
