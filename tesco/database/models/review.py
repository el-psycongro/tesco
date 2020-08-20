
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from tesco.database.connect import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, unique=True)
    product_id = Column('product_id', Integer, ForeignKey('product.product_id'), nullable=False)
    title = Column(String(50), nullable=True)
    stars = Column(Integer, nullable=False)
    author = Column(String(50))
    date = Column(String(20), nullable=False)
    text = Column(String(2000))

    product = relationship("Product", back_populates="review")