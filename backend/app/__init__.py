from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import os

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'DATABASE_URL',
            'postgresql://noteops:noteops@localhost:5432/noteops'
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)
    PrometheusMetrics(app)

    from app.routes.notes import notes_bp
    app.register_blueprint(notes_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
