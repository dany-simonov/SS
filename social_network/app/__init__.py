import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()



def create_app():
    # BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.urandom(24)
    # DEBUG = True

    app = Flask(__name__)
    # app.config.from_object('instance.config')  # Загрузка конфигурации
    app.config.from_object('social_network.app.instance.config.Config')
    print(app.config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # db.create_all()
    migrate.init_app(app, db)

    # Ленивый импорт Blueprints
    from social_network.app.routes import main_bp
    from social_network.app.ai_chat_bp import ai_chat_bp

    # Регистрация Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_chat_bp, url_prefix='/ai-chat')

    return app