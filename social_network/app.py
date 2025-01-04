from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'StudySphere_2024_SuperSecretKey_789@#$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

# Создаем базу при запуске
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
