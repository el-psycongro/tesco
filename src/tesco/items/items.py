# -*- coding: utf-8 -*-

from scrapy import Field, Item
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader


class CustomLoader(ItemLoader):
    default_output_processor = TakeFirst()


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
    title = Field()
    stars = Field()
    author = Field()
    date = Field()
    text = Field()


class UsuallyBoughtNextItem(Item):
    id = Field()
    url = Field()
    image_url = Field()
    title = Field()
    price = Field()
