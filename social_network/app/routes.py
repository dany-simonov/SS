from flask import Blueprint, request, redirect, url_for, jsonify, flash, render_template
from flask_wtf import form
from social_network.app import db
from social_network.app.models import User
from social_network.app.tasks_data import TASKS
from social_network.app.ai_chat import handle_ai_chat
from social_network.app.forms import LoginForm, RegistrationForm


main_bp = Blueprint('main', __name__)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data))
    return redirect(url_for('main.landing'))
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
        return redirect(url_for('main.landing'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/')
def index():
    return redirect(url_for('main.landing'))

@main_bp.route('/landing')
def landing():
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