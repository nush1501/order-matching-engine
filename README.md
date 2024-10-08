# Order Matching API

## Project Overview
This project simulates an order matching engine API, which allows placing, modifying, canceling, and fetching buy and sell orders for an instrument/stock. The system ensures that when bid (buy) and ask (sell) orders match, a trade takes place at the best available price.

The system maintains a **limit order book** and processes each request efficiently. Orders are matched in sequence, and the best bid or ask price is used to determine the trade price.

## Key Concepts

### Limit Order Book
A limit order book is a data structure used to store and manage buy and sell orders. The book is updated whenever an order is placed, modified, or canceled. A trade is executed when a matching buy and sell order is found.

- **Bid Order**: Represents a buyer's offer to purchase a quantity of stock at a maximum price.
- **Ask Order**: Represents a seller's offer to sell a quantity of stock at a minimum price.
- **Order Matching**: A trade occurs when a bid price matches an ask price. The trade price is taken from the order already in the book (ask price for a buy order, and bid price for a sell order).

## Functionalities of the API

1. **Order Operations (CRUD)**:
   - **Place an Order [POST]**: Place a new buy (bid) or sell (ask) order with a specified quantity, price, and side (1 for buy, -1 for sell). Returns an `order_id`.
   - **Modify an Order [PUT]**: Update the price of an existing order using the `order_id`. Returns `success: true/false`.
   - **Cancel an Order [DELETE]**: Cancel an existing order by `order_id`. In case of partial trade, cancels the remaining quantity. Returns `success: true/false`.
   - **Fetch an Order [GET]**: Get details of an existing order including `order_price`, `order_quantity`, `traded_quantity`, and `order_alive` status.
   - **Get All Orders [GET]**: Retrieve all current orders with their details.
   - **Get All Trades [GET]**: Retrieve all trades that have taken place, with details like `trade_price`, `quantity`, and order IDs involved.

2. **Websockets**:
   - **Trade Updates**: Sends a real-time update every time a trade takes place with details like trade price, quantity, and involved orders.
   - **Order Book Snapshots**: Sends a snapshot of the order book every second with 5 levels of bid and ask depth (price and quantity).

## Deliverables
1. **Microservices Design**: The application is broken down into multiple Python-based microservices. You are free to design it and make design decisions to suit performance and scalability.
2. **Documentation**: Include detailed documentation that describes the architecture, data flow, and the purpose of each microservice.
3. **Containerization**: The entire application will be containerized. Include a `docker-compose.yml` file and instructions on how to run the application.
4. **Testing**: Provide either a Postman collection or a simple web interface to test the application.
5. **Crash Recovery**: The application should be able to recover its last state in case of a crash, with a proper restore mechanism.

## Thoughts on Performance
The order book operations are designed to perform in amortized **O(1)** time. Order matching must be done sequentially for maximum throughput, while everything else (like data storage, API handling) can be parallelized or horizontally scaled.

## How to Run the Project
1. Clone the repository.
2. Install dependencies (`pip install -r requirements.txt` or via `Docker`).
3. Use `docker-compose up` to run the application and its services.
4. Test the API using the provided Postman collection or web interface.
