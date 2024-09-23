import enum

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from app.database import Base


class SStatus(Base):
    __tablename__ = 'status_users'
    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String)
    discount = Column(String)


class SUsers(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    status = Column(ForeignKey('status_users.status_id'))
    date_created = Column(DateTime)
    favorit_product = Column(String)


class SShops(Base):
    __tablename__ = 'shops'
    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String)


class Scategories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String)


class SProducts(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    category_id = Column(Integer, ForeignKey('categories.category_id'))


class SQuantity_products(Base):
    __tablename__ = 'quantity_products'
    storage_id = Column(Integer, primary_key=True, autoincrement=True)
    storage_shop = Column(ForeignKey('shops.shop_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)


class SOrders(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime)
    buyer = Column(ForeignKey('users.user_id'))
    shop = Column(ForeignKey('shops.shop_id'))
    product = Column(ForeignKey('products.product_id'))
    quantity = Column(Integer)
    price = Column(Integer)


class OrderStatus(enum.Enum):
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"
