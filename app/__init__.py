from flask import Flask
from app.config import Config
from app.celery_app import create_celery_app
from app.utils import add_global_filters

celery = None

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    global celery
    celery = create_celery_app(app)

    from app.routes import task_bp
    app.register_blueprint(task_bp)

    add_global_filters(app)
    return app