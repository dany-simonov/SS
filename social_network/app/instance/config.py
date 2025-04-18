import os

SECRET_KEY = os.urandom(24)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/app.db'
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join('instance', 'app.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True