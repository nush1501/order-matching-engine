"""
This module defines the Order model for interacting with the order database.

The Order model represents an order in the order matching system and is used
to store order data, including the quantity, price, and order side (buy or sell).
"""

from sqlalchemy import Column, Integer, Float, String
from app.extensions import db  # Import db from extensions


class Order(db.Model):
    """
        Order model representing an order in the database.

        This model defines the structure of the 'orders' table, which stores the
        details of each order, including its quantity, price, and side.

        Attributes:
            id (int): The primary key of the order.
            quantity (int): The number of units in the order.
            price (float): The price per unit of the order.
            side (str): The side of the order ('buy' or 'sell').
        """
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    side = Column(String, nullable=False)
    # ... other fields as needed
