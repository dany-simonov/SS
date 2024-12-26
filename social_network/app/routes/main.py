from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    content = TextAreaField('Контент', validators=[DataRequired()])

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    form = PostForm()
    posts = []  # здесь будут посты из базы данных
    users = []  # здесь будут пользователи из базы данных
    return render_template('index.html', form=form, posts=posts, users=users)
