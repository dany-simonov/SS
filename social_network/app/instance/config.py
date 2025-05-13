import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "app.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'studysphereru@gmail.com'
MAIL_PASSWORD = 'tgvbccecogfmfclm'
MAIL_DEFAULT_SENDER = 'Команда Study Sphere <studysphereru@gmail.com>'