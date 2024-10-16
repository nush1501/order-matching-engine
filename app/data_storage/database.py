from sqlalchemy import create_engine
from app.order_service.models import Order

# Replace with your database connection string
database_url = 'postgresql://user:password@localhost:5432/order_db'

engine = create_engine(database_url)
db.session.configure(bind=engine)
db.create_all()
