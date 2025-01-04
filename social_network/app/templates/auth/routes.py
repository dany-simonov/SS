from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User

# Создаём два Blueprint'а прямо здесь
auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

# Маршруты для auth
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']
        
        if User.query.filter_by(phone=phone).first():
            flash('Такой номер телефона уже зарегистрирован')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Теперь вы можете войти')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        user = User.query.filter_by(phone=phone).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Добро пожаловать!')
            return redirect(url_for('main.profile'))
        flash('Неверный номер телефона или пароль')
    
    return render_template('auth/login.html')

# Маршруты для main
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
