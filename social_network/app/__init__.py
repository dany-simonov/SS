from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # app.config.from_object('instance.config')  # Загрузка конфигурации
    app.config.from_object('social_network.app.instance.config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Ленивый импорт Blueprints
    from social_network.app.routes import main_bp
    from social_network.app.ai_chat_bp import ai_chat_bp

    # Регистрация Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_chat_bp, url_prefix='/ai-chat')

    return app