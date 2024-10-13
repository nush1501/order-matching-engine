from flask import Blueprint, request, jsonify
import logging

from app.matching_service.matcher import Order, order_book

order_bp = Blueprint('order_service', __name__)

logger = logging.getLogger(__name__)


@order_bp.route('/orders', methods=['POST'])
def place_order(db_session):
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

        # Create order
        order = Order(quantity=quantity, price=price, side=side)
        db_session.add(order)
        db_session.commit()

        # Place order in order book
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
    try:
        data = request.json
        updated_price = data.get('updated_price')

        order = Order.query.get(order_id)
        if not order:
            raise ValueError('Order not found')

        order.price = updated_price
        db_session.commit()

        # Update order in order book
        order_book.modify_order(order)

        return jsonify({'success': True}), 200
    except ValueError as e:
        logger.error('Order not found or invalid update: %s', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error('Failed to modify order: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500


@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id, db_session):
    try:
        order = Order.query.get(order_id)
        if not order:
            raise ValueError('Order not found')

        db_session.delete(order)
        db_session.commit()

        # Cancel order in order book
        order_book.cancel_order(order)

        return jsonify({'success': True}), 200
    except ValueError as e:
        logger.error('Order not found: %s', str(e))
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error('Failed to cancel order: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500


@order_bp.route('/orders', methods=['GET'])
def fetch_all_orders():
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error('Failed to fetch all orders: %s', str(e))
        return jsonify({'error': 'Internal server error'}), 500
