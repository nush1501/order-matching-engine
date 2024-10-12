from heapq import heappush, heappop

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}

    def place_order(self, order):
        if order['side'] == 1:  # Buy order
            price = order['price']
            if price not in self.bids:
                self.bids[price] = []
            heappush(self.bids[price], order)
        else:  # Sell order
            price = order['price']
            if price not in self.asks:
                self.asks[price] = []
            heappush(self.asks[price], order)

    def match_orders(self):
        while self.bids and self.asks:
            best_bid_price = max(self.bids.keys())
            best_ask_price = min(self.asks.keys())
            if best_bid_price >= best_ask_price:
                # Match orders
                bid_order = heappop(self.bids[best_bid_price])
                ask_order = heappop(self.asks[best_ask_price])
                # Execute trade logic (update quantities, calculate price, etc.)
                # ...
                # Broadcast trade update
                # ...
            else:
                break


