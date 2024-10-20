"""
Flask application for the order matching engine.

This application handles order management and matching functionality.
It provides API endpoints for placing, fetching, modifying, and canceling orders.

The application leverages blueprints for modularity and organization.
The `order_service` blueprint defines the API endpoints for order management.
"""
from app import create_app

# Create an app instance using the factory function
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
