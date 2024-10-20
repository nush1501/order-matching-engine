"""
This module defines the API endpoints for the order matching engine.
It handles creating, fetching, modifying, and canceling orders.
"""
import logging
from flask import Blueprint, request, jsonify

from ..matching_service.matcher import OrderBook
from .models import Order

order_bp = Blueprint('order_service', __name__)

logger = logging.getLogger(__name__)


@order_bp.route('/orders', methods=['POST'])
def place_order(db_session):
    """
        Place a new order in the order book.

        This endpoint handles the creation of a new order. The request body must
        contain 'quantity', 'price', and 'side' (buy or sell). The function
        validates the input, saves the order to the database, and adds it to
        the order book.

        Args:
            db_session: The active database session.

        Returns:
            JSON response containing the order ID and a status code of 201 if successful.
            If there is an input validation error, returns a JSON error message with a 400 status.
            In case of any other error, returns a 500 status.
        """
    try:
        data = request.json
        print('Hi')
        print(data)
        quantity = data.get('quantity')
        price = data.get('price')
        side = data.get('side')

        # Validate input
        if quantity is None or not isinstance(quantity, int) or quantity < 0:
            raise ValueError('Invalid quantity')
        if price is None or not isinstance(price, float) or price <= 0 or price % 0.01 != 0:
            raise ValueError('Invalid price: Should be a multiple of 0.01')
        if side is None or side not in (1, -1):
            raise ValueError('Invalid side')

        with db_session.begin():
            order = Order(quantity=quantity, price=price, side=side)
            db_session.add(order)
            order_book = OrderBook()  # Create an instance of OrderBook
            order_book.place_order(order)

        return jsonify({'order_id': order.id}), 201
    except ValueError as e:
        logger.error('Invalid input: %s', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error('Failed to place order: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500


@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def fetch_order(order_id):
    """
       Fetch an existing order by its ID.

       This endpoint retrieves a specific order based on the provided order ID.
       It queries the database for the order and returns the order details.

       Args:
           order_id (int): The unique identifier of the order to fetch.

       Returns:
           JSON response with the order details and a 200 status code if found.
           If the order is not found, returns a 404 status with an error message.
           In case of any other error, returns a 500 status.
       """
    try:
        order = Order.query.get(order_id)
        if not order:
            raise ValueError('Order not found')

        return jsonify(order.to_dict()), 200
    except ValueError as e:
        logger.error('Order not found: %s', str(e))
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error('Failed to fetch order: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500


@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
def modify_order(order_id, db_session):
    """
        Modify an existing order's price.

        This endpoint allows updating the price of an existing order. It fetches
        the order by its ID, modifies the price, updates the database, and reflects
        the change in the order book.

        Args:
            order_id (int): The ID of the order to modify.
            db_session: The active database session.

        Returns:
            JSON response with success status and a 200 status if the order is modified successfully.
            If the order is not found or there is an invalid update, returns a 400 status.
            In case of any other error, returns a 500 status.
        """
    try:
        data = request.json
        updated_price = data.get('updated_price')

        order = Order.query.get(order_id)
        if not order:
            raise ValueError('Order not found')

        order.price = updated_price
        db_session.commit()

        # Update order in order book
        order_book = OrderBook()  # Create an instance of OrderBook
        order_book.modify_order(order, updated_price)

        return jsonify({'success': True}), 200
    except ValueError as e:
        logger.error('Order not found or invalid update: %s', str(e))
        return jsonify({'error': str(e)}), 400
    except AttributeError:
        logger.warning('Order book does not support order modification yet')
        return jsonify({'error': 'Order book modification not supported'}), 400
    except Exception as e:
        logger.error('Failed to modify order: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500


@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id, db_session):
    """
        Cancel an existing order.

        This endpoint allows for canceling an order by its ID. It removes the
        order from both the database and the order book.

        Args:
            order_id (int): The ID of the order to cancel.
            db_session: The active database session.

        Returns:
            JSON response with success status and a 200 status if the order is canceled successfully.
            If the order is not found, returns a 404 status with an error message.
            In case of any other error, returns a 500 status.
        """
    try:
        order = Order.query.get(order_id)
        if not order:
            raise ValueError('Order not found')

        db_session.delete(order)
        db_session.commit()

        # Cancel order in order book
        order_book = OrderBook()  # Create an instance of OrderBook
        order_book.remove_order(order)

        return jsonify({'success': True}), 200
    except ValueError as e:
        logger.error('Order not found: %s', str(e))
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error('Failed to cancel order: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500


@order_bp.route('/orders', methods=['GET'])
def fetch_all_orders():
    """
        Fetch all orders.

        This endpoint retrieves all orders from the database and returns them
        in a list format.

        Returns:
            JSON response containing a list of all orders and a 200 status code.
            In case of an error, returns a 500 status.
        """
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error('Failed to fetch all orders: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500
