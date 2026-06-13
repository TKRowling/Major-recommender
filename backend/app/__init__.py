import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate

# Import models so SQLAlchemy can create tables.
from database.models.user import User
from database.models.recommendation_history import RecommendationHistory
from database.models.feedback import Feedback
from database.models.saved_major import SavedMajor
from database.models.chatbot_history import ChatbotHistory


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",

        # Your deployed Vercel frontend
        "https://major-recommender-amber.vercel.app",
    ]

    frontend_url = os.getenv("FRONTEND_URL", "").strip()

    if frontend_url:
        allowed_origins.append(frontend_url.rstrip("/"))

    allowed_origins = list(set(allowed_origins))

    print("Allowed CORS origins:", allowed_origins)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": allowed_origins,
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
        supports_credentials=True,
    )

    @app.route("/")
    def home():
        return jsonify({
            "status": "ok",
            "message": "Major Recommender Backend is running."
        }), 200

    from app.routes.health_routes import health_bp
    from app.routes.recommendation_routes import recommendation_bp
    from app.routes.feedback_routes import feedback_bp
    from app.routes.saved_major_routes import saved_major_bp
    from app.routes.chatbot_history_routes import chatbot_history_bp
    from app.routes.user_routes import user_bp
    from app.routes.chatbot_routes import chatbot_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(recommendation_bp, url_prefix="/api")
    app.register_blueprint(feedback_bp, url_prefix="/api")
    app.register_blueprint(saved_major_bp, url_prefix="/api")
    app.register_blueprint(chatbot_history_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(chatbot_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app