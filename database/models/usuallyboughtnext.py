
from sqlalchemy import Integer, String, DECIMAL, Column, ForeignKey
from sqlalchemy.orm import relationship
from database.connect import Base


class UsuallyBoughtNext(Base):
    __tablename__ = "usually_bought_next"

    id = Column(Integer, primary_key=True, unique=True)
    product_id = Column('product_id', Integer, ForeignKey('product.product_id'), nullable=False)
    url = Column(String(2000), nullable=False)
    image_url = Column(String(2000), nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(DECIMAL)

    product = relationship("Product", back_populates="usually_bought_next")