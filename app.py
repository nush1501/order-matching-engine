"""
Flask application for the order matching engine.

This application handles order management and matching functionality.
It provides API endpoints for placing, fetching, modifying, and canceling orders.

The application leverages blueprints for modularity and organization.
The `order_service` blueprint defines the API endpoints for order management.
"""
from flask import Flask

from app.order_service.routes import order_bp

app = Flask(__name__)

# Register the blueprint

app.register_blueprint(order_bp, url_prefix='/orders')

if __name__ == "__main__":
    app.run(debug=True)
