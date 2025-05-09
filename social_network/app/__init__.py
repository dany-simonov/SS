from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('social_network.app.instance.config')
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Ленивый импорт Blueprints
    from social_network.app.routes import main_bp
    app.register_blueprint(main_bp)
    from social_network.app.ai_chat_bp import ai_chat_bp
    app.register_blueprint(ai_chat_bp, url_prefix='/ai-chat')
    return app