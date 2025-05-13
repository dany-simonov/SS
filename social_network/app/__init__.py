from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('social_network.app.instance.config')
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    from social_network.app.routes import main_bp
    app.register_blueprint(main_bp)

    from social_network.app.ai_chat_bp import ai_chat_bp
    app.register_blueprint(ai_chat_bp, url_prefix='/ai-chat')

    from social_network.app.script import import_tasks
    app.register_blueprint(import_tasks)


    return app