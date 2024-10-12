from flask import Blueprint, request, jsonify

order_routes = Blueprint('order_routes', __name__)

# Simulated in-memory order storage (for demo purposes)
orders = {}
order_id_counter = 1

# Place order
@order_routes.route('/order', methods=['POST'])
def place_order():
    global order_id_counter
    data = request.json
    print(data)
    quantity = data.get('quantity')
    price = data.get('price')
    side = data.get('side')

    # Simple validation
    if quantity <= 0 or price <= 0:
        return jsonify({'error': 'Invalid quantity or price'}), 400

    order_id = order_id_counter
    orders[order_id] = {
        'quantity': quantity,
        'price': price,
        'side': side,
        'order_id': order_id,
        'traded_quantity': 0,
        'average_traded_price': 0.0,
        'alive': True
    }
    order_id_counter += 1
    return jsonify({'order_id': order_id}), 201

# Fetch order
@order_routes.route('/order/<int:order_id>', methods=['GET'])
def fetch_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order), 200

# Cancel order
@order_routes.route('/order/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order['alive'] = False
    return jsonify({'success': True}), 200

# Modify order
@order_routes.route('/order/<int:order_id>', methods=['PUT'])
def modify_order(order_id):
    data = request.json
    updated_price = data.get('updated_price')
    
    order = orders.get(order_id)
    if not order or not order['alive']:
        return jsonify({'error': 'Order not found or already cancelled'}), 404
    
    order['price'] = updated_price
    return jsonify({'success': True}), 200

# Fetch all orders
@order_routes.route('/orders', methods=['GET'])
def fetch_all_orders():
    return jsonify(list(orders.values())), 200

