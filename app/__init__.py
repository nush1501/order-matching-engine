"""
Flask Application Factory Module.

This module contains the application factory function `create_app`,
which initializes and configures a Flask application for the order
matching engine. It sets up the necessary configurations, initializes
the SQLAlchemy database connection, and registers blueprints for handling
the order management routes.

Key Components:
- Configuration: Loads settings from the provided configuration class.
- Database: Initializes the SQLAlchemy database instance.
- Blueprints: Registers the order service blueprint for managing orders.

Usage:
    The `create_app` function can be called to create an instance of
    the Flask application, ready to handle requests related to order
    management.
"""

from flask import Flask
from .extensions import db  # Import db from extensions
from .order_service.routes import order_bp
from .config import DevelopmentConfig  # Import configuration class


def create_app(config_class=DevelopmentConfig):
    """
    Create and configure the Flask application.

    This function sets up the Flask application with the necessary
    configurations, initializes the SQLAlchemy database connection,
    and registers the blueprints for handling routes.

    Args:
        config_class: Configuration class to use (default: DevelopmentConfig)

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(config_class)

    # Initialize extensions (like SQLAlchemy)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(order_bp, url_prefix='/orders')

    return app
