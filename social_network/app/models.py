from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from social_network.app import db


class User(UserMixin, db.Model):
    """
    Модель пользователя для системы аутентификации.

    Поля:
        id (Integer): Уникальный идентификатор пользователя (первичный ключ).
        username (String): Имя пользователя. Не уникальное, но обязательно для заполнения.
        email (String): Электронная почта пользователя. Уникальное поле, обязательно для заполнения.
        password_hash (String): Хэшированный пароль пользователя.
        messages (Relationship): Связь с моделью Message. Представляет сообщения, отправленные пользователем.
        first_name (String): Имя пользователя (необязательное поле).
        last_name (String): Фамилия пользователя (необязательное поле).
        age (Integer): Возраст пользователя (необязательное поле).

    Методы:
        set_password(password): Устанавливает хэшированный пароль для пользователя.
        check_password(password): Проверяет, совпадает ли переданный пароль с хэшированным паролем.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    def set_password(self, password):
        """Устанавливает хэшированный пароль для пользователя."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет, совпадает ли переданный пароль с хэшированным паролем."""
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    """
    Модель сообщений, отправленных пользователями.

    Поля:
        id (Integer): Уникальный идентификатор сообщения (первичный ключ).
        content (String): Текст сообщения. Обязательное поле.
        user_id (Integer): Идентификатор пользователя, отправившего сообщение. Связано с моделью User.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Courses(db.Model):
    """
    Модель курсов для образовательной платформы.

    Поля:
        id (Integer): Уникальный идентификатор курса (первичный ключ).
        course_name (String): Название курса. По умолчанию "_".
        difficulty (Integer): Сложность курса. Обязательное поле.
        title (String): Заголовок курса. Обязательное поле.
        description (Text): Описание курса. Обязательное поле.
        input_example (Text): Пример входных данных для курса. Обязательное поле.
        output_example (Text): Пример выходных данных для курса. Обязательное поле.
    """
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(200), default="_")
    difficulty = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    input_example = db.Column(db.Text, nullable=False)
    output_example = db.Column(db.Text, nullable=False)
