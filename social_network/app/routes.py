from flask import Blueprint, request, redirect, url_for, jsonify, flash, render_template, current_app
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import form
import sqlalchemy as sa
from social_network.app import db, login_manager
from social_network.app.models import User, Courses
from social_network.app.tasks_data import TASKS
from social_network.app.ai_chat import handle_ai_chat
from social_network.app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import LoginManager


@login_manager.user_loader
def load_user(user_id):
    # Загрузка пользователя из базы данных
    return User.query.get(int(user_id))




main_bp = Blueprint('main', __name__)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form)
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        print("=================================")
        print(user)
        print("=================================")
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.account'))
    return render_template('login.html', title='Sign In', form=form)


@main_bp.route('/register', methods=['GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверка, существует ли пользователь с таким email или username
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@main_bp.route('/register', methods=['POST'])
def add_user():
    # print(request.get_data())
    data = request.form
    print("================================================")
    print("================================================")
    print(data)
    print("================================================")
    print("================================================")
    new_user = User()
    new_user.username = data.get('username')
    new_user.email = data.get('email')
    new_user.set_password(data.get('password'))

    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/')
def index():
    return redirect(url_for('main.landing'))

@main_bp.route('/landing')
def landing():
    print("========================================================")
    print("========================================================")
    print(current_app.config["BASE_DIR"])
    print("========================================================")
    print("========================================================")
    return render_template('landing.html')

@main_bp.route('/textbook')
def textbook():
    return render_template('textbook.html')

@main_bp.route('/tasks')
def show_tasks():
    return render_template('tasks.html', tasks=TASKS)

@main_bp.route('/task_view')
def task_view():
    task_title = request.args.get('title')
    return render_template('task_view.html', task_title=task_title)

@main_bp.route('/support', methods=['GET'])
def support():
    return render_template('support.html')

@main_bp.route('/execute-code', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    try:
        local_dict = {}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        output = local_dict.get('result', 'Код выполнен успешно')
        return jsonify({'success': True, 'output': output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


ai_chat_bp = Blueprint('ai_chat', __name__)


@ai_chat_bp.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    if request.method == 'POST':
        return handle_ai_chat(request)
    return render_template('ai_chat.html')


@main_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    print(current_user)
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data or None
        current_user.last_name = form.last_name.data or None
        current_user.age = form.age.data or None

        db.session.commit()

    return render_template('account.html', form=form, user=current_user)


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main_bp.route('/my-courses')
def my_courses():
    return render_template('courses.html', form=form)