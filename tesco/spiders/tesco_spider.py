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

    @staticmethod
    def get_requests(name=name):
        with open('requests_links.json', 'r', encoding='utf-8') as links_json:
            json_data = json.load(links_json)
            if name in json_data:
                return list(map(scrapy.Request, json_data[name]))
            return 0

    rules = (
        # RULE: following each product and parse data
        Rule(LinkExtractor(
           restrict_xpaths='//ul[@class="product-list grid"]//div[@class="tile-content"]/a'), callback='parse_product',
           follow=True),
        # RULE: follow next reviews page and parse
        Rule(LinkExtractor(
            restrict_xpaths='//div[@data-auto="review-list-container"]/div[2]/p[2]/a'), callback='parse_review',
            follow=True),
        # # RULE: open new page with product list
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

        product_id = self._parse_id(product_json_data)
        loader.add_value('id', product_id)

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
                loader_bought_next.add_value('id', product_id)
                loader_bought_next.add_value('url', 'https://www.tesco.com/groceries/en-GB/products/' + product)
                loader_bought_next.add_value('image_url', product_data['defaultImageUrl'])
                loader_bought_next.add_value('title', product_data['title'])
                loader_bought_next.add_value('price', product_data['price'])
                yield loader_bought_next.load_item()

        # PARSE REVIEW
        yield from self.parse_review(response)

    def parse_review(self, response, json_data=None):
        if json_data is None:
            str_json_data = response.xpath('//body/@data-redux-state').get()
            json_data = self.get_json_load_data(str_json_data)

        loader = CustomLoader(item=ReviewItem(), response=response)
        product_id = json_data['productDetails']['product']['id']
        reviews = json_data['productDetails']['product']["reviews"]["entries"]
        for review in reviews:
            loader.add_value('id', product_id)
            title = review["summary"] if review["summary"] else 'None'
            loader.add_value('title', title)
            loader.add_value('stars', review["rating"]["value"])
            author = review["syndicationSource"]["name"] if review["syndicated"] else 'A Tesco Customer'
            loader.add_value('author', author)
            loader.add_value('date', review["submissionTime"])
            loader.add_value('text', review["text"] if review["text"] else 'None')
            yield loader.load_item()

    @staticmethod
    def _parse_id(product_json_data):
        product_id = product_json_data['id']
        return product_id

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
