"""
Application Factory — Patrón Flask Application Factory.
Centraliza la creación y configuración de la app Flask.
"""
import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_app() -> Flask:
    """Crea y configura la aplicación Flask."""
    configure_logging()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )

    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

    # CORS
    CORS(app)

    # Registrar blueprints
    from src.interfaces.api.routes.api_routes import api_bp
    from src.interfaces.web.web_routes import web_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    # Handler de errores global
    @app.errorhandler(404)
    def not_found(e):
        from flask import jsonify
        return jsonify({"error": "Endpoint no encontrado"}), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import jsonify
        return jsonify({"error": "Error interno del servidor"}), 500

    return app