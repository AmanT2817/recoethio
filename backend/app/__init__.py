from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .db_init import init_db

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.items import items_bp
    from .routes.ratings import ratings_bp
    from .routes.recommendations import recommendations_bp
    from .routes.wishlist import wishlist_bp
    from .routes.search import search_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(ratings_bp, url_prefix='/api/ratings')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    app.register_blueprint(wishlist_bp, url_prefix='/api/wishlist')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Initialize database on app startup
    with app.app_context():
        init_db()

    return app
