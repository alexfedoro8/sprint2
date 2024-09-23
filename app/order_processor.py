# app/order_processor.py

import pika
import json
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SOrders, SQuantity_products, OrderStatus
from app.shemas import OrderCreate
from datetime import datetime

RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/'


async def create_order(order: OrderCreate, db: Session):
    new_order = SOrders(
        buyer=order.buyer_id,
        shop=order.shop_id,
        product=order.product_id,
        quantity=order.quantity,
        price=order.price,
        date_created=datetime.now()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_data = {
        "order_id": new_order.order_id,  # берем из базы primary key
        "buyer_id": new_order.buyer,
        "shop_id": new_order.shop,
        "product_id": new_order.product,
        "quantity": new_order.quantity,
        "price": new_order.price,
        "date_created": new_order.date_created
    }

    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.basic_publish(
        exchange='',
        routing_key='new_orders_queue',
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

    return {"message": "Order created successfully", "order_id": new_order.order_id}


class OrderProcessor:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        self.channel = self.connection.channel()

        # Объявляем очереди
        self.channel.queue_declare(queue='new_orders_queue', durable=True)
        self.channel.queue_declare(queue='process_orders_queue', durable=True)
        self.channel.queue_declare(queue='notifications_queue', durable=True)

    def process_new_order(self, ch, method, properties, body):
        order_data = json.loads(body)
        print(f"Received new order: {order_data}")

        self.channel.basic_publish(
            exchange='',
            routing_key='process_orders_queue',
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_order(self, ch, method, properties, body):
        order_data = json.loads(body)
        print(f"Processing order data: {order_data}")

        with next(get_db()) as db:
            self.update_order_status(db, order_data, OrderStatus.PROCESSING)
            self.save_order_to_db(db, order_data)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        # Уведомление
        notification = {
            "user_id": order_data['buyer_id'],
            "message": "Your order has been processed successfully."
        }
        self.channel.basic_publish(
            exchange='',
            routing_key='notifications_queue',
            body=json.dumps(notification),
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def save_order_to_db(self, db: Session, order_data: dict):
        order = db.query(SOrders).filter(SOrders.order_id == order_data['order_id']).first()
        if order:
            self.update_product_quantity(db, order_data)
            self.update_order_status(db, order_data, OrderStatus.COMPLETED)

    def update_product_quantity(self, db: Session, order_data: dict):
        product_stock = db.query(SQuantity_products).filter(
            SQuantity_products.product_id == order_data['product_id'],
            SQuantity_products.storage_shop == order_data['shop_id']
        ).first()

        if product_stock and product_stock.quantity >= order_data['quantity']:
            product_stock.quantity -= order_data['quantity']
            db.commit()
        else:
            print(f"Insufficient quantity for product {order_data['product_id']} in shop {order_data['shop_id']}")
            self.update_order_status(db, order_data, OrderStatus.CANCELED)

    def update_order_status(self, db: Session, order_data: dict, status: OrderStatus):
        order = db.query(SOrders).filter(SOrders.order_id == order_data['order_id']).first()
        if order:
            order.status = status
            db.commit()
        else:
            print(f"Order with ID {order_data['order_id']} not found.")

    def process_notification(self, ch, method, properties, body):
        notification = json.loads(body)
        print(f"Sending notification to user {notification['user_id']}: {notification['message']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(queue='new_orders_queue', on_message_callback=self.process_new_order)
        self.channel.basic_consume(queue='process_orders_queue', on_message_callback=self.process_order)
        self.channel.basic_consume(queue='notifications_queue', on_message_callback=self.process_notification)

        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()
        self.connection.close()
