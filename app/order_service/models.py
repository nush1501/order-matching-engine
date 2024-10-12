# app/order_service/models.py
from sqlalchemy import Column, Integer, Float, Boolean, String

class Order(db.Model):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    side = Column(String, nullable=False)
    # ... other fields as needed