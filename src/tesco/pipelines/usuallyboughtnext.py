from sqlalchemy.orm import sessionmaker
from tesco.database.connect import engine
from tesco.database.models.usuallyboughtnext import UsuallyBoughtNext
from tesco.items.items import UsuallyBoughtNextItem


class UsuallyBoughtNextPipeline:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        usually_bought_next = UsuallyBoughtNext()
        if isinstance(item, UsuallyBoughtNextItem):
            usually_bought_next.product_id = item['id']
            usually_bought_next.url = item['url']
            usually_bought_next.image_url = item['image_url']
            usually_bought_next.title = item['title']
            usually_bought_next.price = item['price']

            try:
                self.session.add(usually_bought_next)
                self.session.commit()
            except:
                self.session.rollback()
                raise
        return item

    def close_spider(self, spider):
        self.session.close()
