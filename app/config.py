"""
Configuration Module for Flask Application.

This module defines configuration classes for the Flask application,
specifically for different environments such as development and production.
It includes the base configuration class and environment-specific settings.

Classes:
- Config: The base configuration class containing shared settings.
- DevelopmentConfig: Configuration settings for the development environment.
- ProductionConfig: Configuration settings for the production environment.

Key Settings:
- SQLALCHEMY_DATABASE_URI: Specifies the database URI for SQLAlchemy.
- SQLALCHEMY_TRACK_MODIFICATIONS: Disables Flask-SQLAlchemy's modification tracking for performance.

Usage:
    To use a specific configuration, import the desired class and pass it
    to the Flask application's `config.from_object` method.
"""
class Config:
    """Base configuration class."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///orders.db'  # Default database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
