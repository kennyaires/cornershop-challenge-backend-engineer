from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint



Base = declarative_base()


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    store = Column(String, nullable=False)
    barcodes = Column(String, nullable=True)
    sku = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    package = Column(String, nullable=True)
    image_urls = Column(String, nullable=True)

    branch_products = relationship("BranchProduct", back_populates="product")

    __table_args__ = (UniqueConstraint('store', 'sku', name='_store_sku_unique'),)


class BranchProduct(Base):

    __tablename__ = 'branchproducts'

    id = Column(Integer, primary_key=True)
    product_id = Column(None, ForeignKey('products.id'), nullable=False)
    branch = Column(String, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    price = Column(Float, nullable=False)

    product = relationship("Product", back_populates="branch_products")
