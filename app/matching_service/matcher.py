"""
This module implements an order book for an order matching engine.

It defines classes for managing price levels, placing and modifying orders,
and matching buy and sell orders. The `OrderBook` class uses a Red-Black Tree
to maintain orders and supports operations such as placing, modifying,
removing, and matching orders.

Classes:
    - PriceLevelIndex: Manages price levels and associated orders.
    - OrderBook: Handles order placement, modification, and matching.
    - Trade: Represents a trade transaction between buy and sell orders.
"""
from collections import defaultdict
from bintrees import RBTree


class PriceLevelIndex:
    def __init__(self):
        self.index = defaultdict(list)

    def add_order(self, price, node):
        self.index[price].append(node)

    def remove_order(self, price, node):
        self.index[price].remove(node)
        if not self.index[price]:
            del self.index[price]

    def get_nodes_at_price(self, price):
        return self.index.get(price, [])


class OrderBook:
    """
       Class representing an order book for managing buy and sell orders.

       Attributes:
           buy_orders (RBTree): Red-Black Tree for buy orders.
           sell_orders (RBTree): Red-Black Tree for sell orders.
           price_index (PriceLevelIndex): Manages the index of price levels.
       """
    def __init__(self):
        self.buy_orders = RBTree()  # Red-Black Tree for buy orders (price as key)
        self.sell_orders = RBTree()  # Red-Black Tree for sell orders (price as key)
        self.price_index = PriceLevelIndex()

    def place_order(self, order):
        """Place a new order in the order book."""
        tree = self.buy_orders if order.side == 1 else self.sell_orders
        node = tree.insert(order.price, order)
        self.price_index.add_order(order.price, node)

    def match_orders(self):
        """Match buy and sell orders based on their prices."""
        trades = []
        while self.buy_orders and self.sell_orders:
            buy_price = self.buy_orders.min_key()
            sell_price = self.sell_orders.min_key()

            if buy_price >= sell_price:
                buy_orders = self.price_index.get_nodes_at_price(buy_price)
                sell_orders = self.price_index.get_nodes_at_price(sell_price)

                for buy_order in buy_orders:
                    for sell_order in sell_orders:
                        if self.match_order_pair(buy_order, sell_order, trades):
                            break  # Stop iterating once a match is found

            # Remove empty price levels from the index
            if not self.buy_orders.get(buy_price):
                self.buy_orders.delete(buy_price)
                self.price_index.remove_order(buy_price, None)
            if not self.sell_orders.get(sell_price):
                self.sell_orders.delete(sell_price)
                self.price_index.remove_order(sell_price, None)

        return trades

    def match_order_pair(self, buy_order, sell_order, trades):
        """Match a single pair of buy and sell orders."""
        if buy_order.price < sell_order.price:
            return False

        trade_quantity = min(buy_order.quantity, sell_order.quantity)
        buy_order.quantity -= trade_quantity
        sell_order.quantity -= trade_quantity

        # Handle order cancellation (if either quantity becomes 0)
        if buy_order.quantity == 0:
            self.remove_order(buy_order)
        if sell_order.quantity == 0:
            self.remove_order(sell_order)

        trade = Trade(buy_order_id=buy_order.id, sell_order_id=sell_order.id, price=sell_order.price,
                      quantity=trade_quantity)
        trades.append(trade)
        return True

    def remove_order(self, order):
        """Remove an order from the order book."""
        tree = self.buy_orders if order.side == 1 else self.sell_orders
        node = tree.delete(order.price, order)
        self.price_index.remove_order(order.price, node)

    def modify_order(self, order, new_price):
        """
        Modifies the price of an existing order in the order book.

        Args:
            order (Order): The order object with updated price.
            new_price (float): The new price to assign to the order.
        """

        # Check if order exists in the correct tree (buy/sell)
        tree = self.buy_orders if order.side == 1 else self.sell_orders
        if order not in tree:
            raise ValueError(f"Order with ID {order.id} not found in {tree.name} orders")

        # Update order price and re-insert into the tree
        old_price = order.price
        order.price = new_price

        # Remove the order from the current price level
        self.price_index.remove_order(old_price, tree.get(old_price, None))

        # Re-insert the order with the updated price
        tree.insert(order.price, order)
        self.price_index.add_order(order.price, tree[order.price])


class Trade:
    """
    Represents a trade between a buy and sell order.
    """

    def __init__(self, buy_order_id, sell_order_id, price, quantity):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.price = price
        self.quantity = quantity
