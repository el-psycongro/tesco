import scrapy
import unicodedata
import json
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from tesco.items.items import ProductItem, UsuallyBoughtNextItem, ReviewItem, CustomLoader


class TescoSpider(CrawlSpider):
    name = 'tesco'
    allowed_domains = ['www.tesco.com']

    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9,ru-UA;q=0.8,ru;q=0.7,uk-US;q=0.6,uk;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Host': 'www.tesco.com',
            'Connection': 'keep-alive',
        }
    }

    def start_requests(self):
        for request in self.get_requests(name=self.name):
            yield request

    rules = (
        # RULE: following each product and parse data
        Rule(LinkExtractor(
            restrict_xpaths='//ul[@class="product-list grid"]//div[@class="tile-content"]/a'), callback='parse_product',
            follow=True),
        # RULE: open new page with product list
        Rule(LinkExtractor(
            restrict_xpaths='//nav[@class="pagination--page-selector-wrapper"]//li[last()]/a'), follow=True),
    )

    def parse_product(self, response):
        loader = CustomLoader(item=ProductItem(), response=response)

        str_json_data = response.xpath('//body/@data-redux-state').get()
        json_data = self.get_json_load_data(str_json_data)
        product_json_data = json_data['productDetails']['product']

        url = response.url
        loader.add_value('url', url)

        _id = self._parse_id(product_json_data)
        loader.add_value('id', _id)

        image_url = self._parse_image_url(product_json_data)
        loader.add_value('image_url', image_url)

        title = self._parse_title(product_json_data)
        loader.add_value('title', title)

        category = self._parse_category(product_json_data)
        loader.add_value('category', category)

        price = self._parse_price(product_json_data)
        loader.add_value('price', price)

        description = self._parse_description(product_json_data)
        loader.add_value('description', description)

        name_and_address = self._parse_name_and_address(product_json_data)
        loader.add_value('name_and_address', name_and_address)

        return_address = self._parse_return_address(product_json_data)
        loader.add_value('return_address', return_address)

        net_contents = self._parse_net_content(product_json_data)
        loader.add_value('net_contents', net_contents)

        yield loader.load_item()

        # PARSE USUALLY BOUGHT NEXT PRODUCTS
        if json_data['recommendations']['tescoRecommendations'] is not None:
            loader_bought_next = CustomLoader(item=UsuallyBoughtNextItem(), response=response)
            next_products = json_data['recommendations']['tescoRecommendations'][product_json_data['baseProductId']]['productItems']['serializedData']
            for product in next_products['_keys']:
                product_data = next_products[product]['serializedData']['product']['serializedData']
                loader_bought_next.add_value('id', _id)
                loader_bought_next.add_value('url', 'https://www.tesco.com/groceries/en-GB/products/' + product)
                loader_bought_next.add_value('image_url', product_data['defaultImageUrl'])
                loader_bought_next.add_value('title', product_data['title'])
                loader_bought_next.add_value('price', product_data['price'])
                yield loader_bought_next.load_item()

        # PARSE REVIEW
        yield scrapy.Request(url=response.url, callback=self.parse_review, meta={'id': _id}, dont_filter=True)

    def parse_review(self, response):
        loader = CustomLoader(item=ReviewItem(), response=response)

        reviews = response.xpath('//article[@class="content"]/section')
        product_id = response.meta['id']
        for review in reviews:
            title = review.xpath('./h4/text()').get()
            stars = review.xpath('./div/@aria-label').get()
            stars = stars.split(' ')[0] if stars else None
            author = review.xpath('./p[1]/text()').get()
            if author is None:
                author = review.xpath('.//span[@class="nickname"]/text()').get()
            date = review.xpath('./p/span[@class="submission-time"]/text()').get()
            text = review.xpath('./p[last()]/text()').get()

            loader.replace_value('id', product_id)
            loader.replace_value('title', title)
            loader.replace_value('stars', stars)
            loader.replace_value('author', author)
            loader.replace_value('date', date)
            loader.replace_value('text', text)

            yield loader.load_item()

        next_review_page = response.xpath('//div[@data-auto="review-list-container"]/div[2]/p[2]/a/@href').get()
        if next_review_page is not None:
            yield response.follow(url=next_review_page, callback=self.parse_review, meta={'id': product_id}, dont_filter=True)

    @staticmethod
    def _parse_id(product_json_data):
        _id = product_json_data['id']
        return _id

    @staticmethod
    def _parse_image_url(product_json_data):
        image_url = product_json_data['defaultImageUrl']
        image_url = image_url[:image_url.find('?')]
        return image_url

    @staticmethod
    def _parse_title(product_json_data):
        title = product_json_data['title']
        return title

    @staticmethod
    def _parse_category(product_json_data):
        category = product_json_data['departmentName']
        return category

    @staticmethod
    def _parse_price(product_json_data):
        price = product_json_data['price']
        return price

    @staticmethod
    def _parse_description(product_json_data):
        description = product_json_data['description']
        if len(description) > 0:
            description = "".join(description)
            return description
        return None

    @staticmethod
    def _parse_name_and_address(product_json_data):
        if product_json_data['manufacturerAddress']:
            values_list = product_json_data['manufacturerAddress'].values()
            name_and_address = ''.join(value for value in values_list if value)
            return name_and_address
        else:
            return None

    @staticmethod
    def _parse_return_address(product_json_data):
        if product_json_data['returnTo']:
            values_list = product_json_data['returnTo'].values()
            return_address = ''.join(value for value in values_list if value)
            return return_address
        else:
            return None

    @staticmethod
    def _parse_net_content(product_json_data):
        net_content = product_json_data['details']['netContents']
        return net_content

    @staticmethod
    def get_json_load_data(str_json):
        new_str = str_json.strip()
        new_str = bytes(new_str, 'utf-8').decode('utf-8', 'ignore')
        new_str = unicodedata.normalize('NFD', new_str)
        new_str = new_str.replace('\r', '')
        new_str = new_str.replace('\n', '')
        new_str = new_str.replace('\a', '')
        new_str = new_str.replace('\t', '')
        new_str = new_str.replace('\u2019', '`')
        new_str = new_str.replace('\u0301', '')
        new_str = new_str.replace('\u212e', 'e')
        json_data = json.loads(new_str)
        return json_data

    def get_requests(self, name=name):
        with open('requests_links.json', encoding='utf-8') as links_json:
            json_data = json.load(links_json)
            for link in json_data[name]:
                yield scrapy.Request(link, dont_filter=True)