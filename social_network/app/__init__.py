"""
Этот модуль инициализирует и настраивает приложение Flask вместе с его расширениями.

Он настраивает следующие компоненты:
- SQLAlchemy для управления базой данных.
- Flask-Migrate для обработки миграций базы данных.
- Flask-Login для аутентификации пользователей.
- Flask-Mail для отправки электронных писем.
- Блюпринты для модульного разделения маршрутов.

Функция `create_app` является основной точкой входа для инициализации приложения Flask.
"""
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
"""
Экземпляр SQLAlchemy для управления операциями с базой данных.
"""

login_manager = LoginManager()
"""
Экземпляр LoginManager из Flask-Login для обработки аутентификации пользователей.
"""

migrate = Migrate()
"""
Экземпляр Flask-Migrate для управления миграциями схемы базы данных.
"""

mail = Mail()
"""
Экземпляр Flask-Mail для отправки электронных писем.
"""


def create_app(conf='social_network.app.instance.config'):
    """
    Создает и настраивает новое приложение Flask.

    Эта функция инициализирует приложение Flask, настраивает его с использованием предоставленной конфигурации
    и регистрирует все необходимые расширения и блюпринты.

    Аргументы:
        conf (str): Путь к объекту конфигурации. По умолчанию 'social_network.app.instance.config'.

    Возвращает:
        Flask: Полностью настроенное приложение Flask.
    """
    app = Flask(__name__)
    app.config.from_object(conf)
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

    from social_network.app.quizzes_bp import quizzes_bp
    app.register_blueprint(quizzes_bp)

    return app