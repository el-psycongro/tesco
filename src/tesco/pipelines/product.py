
from sqlalchemy.orm import sessionmaker
from tesco.database.models.product import Product
from tesco.database.connect import engine
from tesco.items.items import ProductItem


class ProductPipeline:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        product = Product()
        if isinstance(item, ProductItem):
            product.product_id = item['id']
            product.url = item['url']
            product.image_url = item['image_url']
            product.title = item['title']
            product.category = item['category']
            product.price = item['price']
            product.description = item['description']
            product.name_and_address = item['name_and_address']
            product.return_address = item['return_address']
            product.net_contents = item['net_contents']

            try:
                self.session.add(product)
                self.session.commit()
            except:
                self.session.rollback()
                raise

        return item

    def close_spider(self, spider):
        self.session.close()
