from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..order_service.models import Order
import datetime

# Replace with your database connection string
database_url = 'postgresql://user:password@localhost:5432/order_db'

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    buy_order_id = Column(Integer, ForeignKey('orders.id'))
    sell_order_id = Column(Integer, ForeignKey('orders.id'))
    price = Column(Float)
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)


# Create all database tables (including the new 'trades' table)
Base.metadata.create_all(engine)