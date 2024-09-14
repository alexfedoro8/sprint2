# from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, ForeignKey
# from datetime import datetime
#
# metadata = MetaData()
#
# #коструктор таблицы статусов
# status_users = Table('status_users', metadata,
#                      Column('status_id', Integer, primary_key=True),
#                      Column('status_name', String(255), nullable=False),
#                      Column('discount', String(255), nullable=False),
#                      )
#
# # конструктор таблицы пользователей (id, имя пользователя, пароль,  e-mail, телефон, статус пользователя, дата регистрации, избранное)
# users = Table('users', metadata,
#               Column('user_id', Integer, primary_key=True),
#               Column('user_name', String(255), nullable=False),
#               Column('password', String(255), nullable=False),
#               Column('email', String(255), nullable=False),
#               Column('telephone', String(255), nullable=False),
#               Column('status', ForeignKey(status_users.c.status_id), nullable=False),
#               Column('date_registered', DateTime, nullable=False),
#               Column('favorit_product', String(255), nullable=False),
# )
#
# # конструктор таблицы магазины( id, название магазина)
# shops = Table('shops', metadata,
#               Column('shop_id', Integer, primary_key=True),
#               Column('shop_name', String(255), nullable=False),
# )
#
# # конструктор таблицы категории(id, название категории)
# categories = Table('categories', metadata,
#                    Column('category_id', Integer, primary_key=True),
#                    Column('category_name', String(255), nullable=False),
# )
#
# #конструктор таблицы продукты (id, название продукта, категория внешний ключ)
# products = Table('products', metadata,
#                  Column('product_id', Integer, primary_key=True),
#                  Column('product_name', String(255), nullable=False),
#                  Column('category_id', ForeignKey('categories.category_id'), nullable=False),
# )
#
# # конструктор таблицы остатки товаров(склад магазина, id продукта, оставшееся количество товара)
# products_quantity = Table('products_quantity', metadata,
#                           Column('store_warehouse', ForeignKey('shops.shop_id')),
#                           Column('product_id', Integer, ForeignKey('products.product_id'), nullable=False),
#                           Column('price', Integer, nullable=False),
#                           Column('quantity', Integer, nullable=False),
# )
# # конструктор таблицы заказы(id заказа, id юзера, где купил, что купил, сколько купил)
# orders = Table('orders', metadata,
#                Column('order_id', Integer, primary_key=True),
#                Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
#                Column('shop_id', Integer, ForeignKey('shops.shop_id'), nullable=False),
#                Column('product_id', Integer, ForeignKey('products.product_id'), nullable=False),
#                Column('quantity', Integer, nullable=False),
#                Column('price', Integer, nullable=False),
#                )
