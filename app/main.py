from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.shemas import OrderCreate
from app.order_processor import OrderProcessor, create_order
import threading

app = FastAPI()

@app.post("/orders/create")
async def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return await create_order(order, db)

# Запуск процесса обработки заказов
def start_order_processing():
    processor = OrderProcessor()
    processor.start_consuming()

threading.Thread(target=start_order_processing, daemon=True).start()
