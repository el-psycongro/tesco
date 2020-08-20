# -*- coding: utf-8 -*-

from scrapy import Field, Item
from scrapy.loader.processors import TakeFirst, Compose
from scrapy.loader import ItemLoader
from datetime import datetime


class CustomLoader(ItemLoader):
    default_output_processor = Compose(lambda v: v[-1])


def epoch_to_date(value):
    date = datetime.utcfromtimestamp(value/1000.).strftime('%Y %m %d')
    return date


class ProductItem(Item):
    url = Field()
    id = Field()
    image_url = Field()
    title = Field()
    category = Field()
    price = Field()
    description = Field()
    name_and_address = Field()
    return_address = Field()
    net_contents = Field()


class ReviewItem(Item):
    id = Field()
    title = Field(default=None)
    stars = Field()
    author = Field()
    date = Field(output_processor=Compose(lambda v: v[-1], epoch_to_date))
    text = Field()


class UsuallyBoughtNextItem(Item):
    id = Field()
    url = Field()
    image_url = Field()
    title = Field()
    price = Field()
