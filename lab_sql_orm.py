#Laboratorium 4

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

cart_product_association = Table(
    'cart_product_association',
    Base.metadata,
    Column('cart_id', Integer, ForeignKey('cart.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True)
)

class users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)

class shipping_address(Base):
    __tablename__ = 'shipping_address'

    shipping_address_id = Column(Integer, primary_key=True)
    country = Column(String)
    city = Column(String)
    postal_code = Column(String)
    block_number = Column(String)
    apartment_number = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="shipping_address")

class carts(Base):
    __tablename__ = 'cart'

    user_id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    creation_date = Column(DateTime)

    user = relationship("User", back_populates="carts")
    products = relationship("Product", secondary=cart_product_association, back_populates="carts")

class product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True)
    title = Column(String())
    description = Column(String)
    price = Column(Float)

    carts = relationship("Cart", secondary=cart_product_association, back_populates="products")