
from sqlalchemy.orm import sessionmaker
from database.connect import engine
from database.models.review import Review
from tesco.items import ReviewItem


class ReviewPipeline:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        review = Review()
        if isinstance(item, ReviewItem):
            review.product_id = item['id']
            review.title = item['title']
            review.stars = item['stars']
            review.author = item['author']
            review.date = item['date']
            review.text = item['text']

            try:
                self.session.add(review)
                self.session.commit()
            except:
                self.session.rollback()
                raise

        return item

    def close_spider(self, spider):
        self.session.close()
