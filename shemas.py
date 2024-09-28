from pydantic import BaseModel


class OrderCreate(BaseModel):
    buyer_id: int
    shop_id: int
    product_id: int
    quantity: int
    price: int
