from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    phone = StringField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('auth/register.html', form=form)
