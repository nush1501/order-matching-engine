from flask import Flask

from app.order_service.routes import order_bp

app = Flask(__name__)

# Register the blueprint
# app.register_blueprint(order_bp, url_prefix='/orders')

if __name__ == "__main__":
    app.run(debug=True)
