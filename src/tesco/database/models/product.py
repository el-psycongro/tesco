
from sqlalchemy import Integer, String, DECIMAL, Column
from sqlalchemy.orm import relationship
from tesco.database.connect import Base


class Product(Base):
    __tablename__ = "product"

    product_id = Column('product_id', Integer, primary_key=True, nullable=False, unique=True)
    url = Column('url', String(2000), nullable=False)
    image_url = Column('image_url', String(2000), nullable=False)
    title = Column('title', String(255), nullable=False)
    category = Column('category', String(255), nullable=False)
    price = Column('price', DECIMAL())
    description = Column('description', String(5000))
    name_and_address = Column('name_and_address', String(1000))
    return_address = Column('return_address', String(1000))
    net_contents = Column('net_contents', String(1000))

    review = relationship("Review", back_populates="product")
    usually_bought_next = relationship("UsuallyBoughtNext", back_populates="product")

