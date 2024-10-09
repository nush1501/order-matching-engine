from flask import Flask
from order_service.routes import order_routes

app = Flask(__name__)

# Register the order routes
app.register_blueprint(order_routes)

if __name__ == "__main__":
    app.run(debug=True)
