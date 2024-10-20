"""
This module initializes the SQLAlchemy database instance for the Flask application.

The `db` object acts as the primary interface for interacting with the database,
providing methods to query and manage data within the application.

Usage:
    - Import the `db` instance to define models or perform database operations.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()
