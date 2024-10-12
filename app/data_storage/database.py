# app/data_storage/database.py
from sqlalchemy import create_engine
from app.order_service.models import Order

engine = create_engine('postgresql://user:password@host:port/database')
db.session.configure(bind=engine)
db.create_all()