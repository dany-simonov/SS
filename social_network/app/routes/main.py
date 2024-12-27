from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Post, User
from app.forms.post_forms import PostForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    users = User.query.all()
    return render_template('index.html', form=form, posts=posts, users=users)

@bp.route('/landing')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('landing.html')

@bp.route('/create_post', methods=['POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост опубликован!')
    return redirect(url_for('main.index'))

@bp.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).all()
    return render_template('user_profile.html', user=user, posts=posts)
