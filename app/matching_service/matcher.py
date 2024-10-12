class Order:
    """
    Represents an order in the order book.
    """

    def __init__(self, order_id, user_id, side, price, quantity):
        self.id = order_id
        self.user_id = user_id
        self.side = side  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity

class OrderBook:
    """
    Implements an order book for buy and sell orders.
    """

    def __init__(self):
        self.buy_orders = []  # List of buy orders (highest price first)
        self.sell_orders = []  # List of sell orders (lowest price first)

    def place_order(self, order):
        """
        Places an order in the appropriate side of the order book.
        """

        if order.side == 'buy':
            # Insert order at appropriate position (highest price first)
            for i, existing_order in enumerate(self.buy_orders):
                if order.price >= existing_order.price:
                    self.buy_orders.insert(i, order)
                    return
            self.buy_orders.append(order)
        else:  # Sell order
            # Insert order at appropriate position (lowest price first)
            for i, existing_order in enumerate(self.sell_orders):
                if order.price <= existing_order.price:
                    self.sell_orders.insert(i, order)
                    return
            self.sell_orders.append(order)

    def match_orders(self):
        """
        Matches buy and sell orders based on price and quantity.
        """

        trades = []
        while self.buy_orders and self.sell_orders:
            # Get top buy and sell orders
            buy_order = self.buy_orders[-1]
            sell_order = self.sell_orders[0]

            # Check if prices match or buy price is higher than sell price
            if buy_order.price >= sell_order.price:
                # Calculate trade quantity (min of buy and sell order quantities)
                trade_quantity = min(buy_order.quantity, sell_order.quantity)

                # Update order quantities
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity

                # Create trade object
                trade = Trade(buy_order_id=buy_order.id, sell_order_id=sell_order.id, price=sell_order.price, quantity=trade_quantity)
                trades.append(trade)

                # Remove fully executed orders
                if buy_order.quantity == 0:
                    self.buy_orders.pop()
                if sell_order.quantity == 0:
                    self.sell_orders.pop(0)

        return trades

class Trade:
    """
    Represents a trade between a buy and sell order.
    """

    def __init__(self, buy_order_id, sell_order_id, price, quantity):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.price = price
        self.quantity = quantity

# Example usage
order_book = OrderBook()

order_1 = Order(1, 101, 'buy', 100, 10)
order_2 = Order(2, 102, 'sell', 98, 5)
order_3 = Order(3, 103, 'buy', 102, 20)

order_book.place_order(order_1)
order_book.place_order(order_2)
order_book.place_order(order_3)

trades = order_book.match_orders()

for trade in trades:
    print(f"Trade: Buy Order ID: {trade.buy_order_id}, Sell Order ID: {trade.sell_order_id}, Price: {trade.price}, Quantity: {trade.quantity}")