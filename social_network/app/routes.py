import sqlalchemy as sa
from flask import Blueprint, request, redirect, url_for, jsonify, flash, render_template, current_app, Flask
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import form
from social_network.app import db, login_manager
from social_network.app.ai_chat import handle_ai_chat
from social_network.app.forms import LoginForm, RegistrationForm, EditProfileForm
from social_network.app.models import User
from social_network.app.tasks_data import TASKS
from .sendemail import send_email

@login_manager.user_loader
def load_user(user_id):
    """
    Загружает пользователя по его ID.

    Args:
        user_id (int): Уникальный идентификатор пользователя.

    Returns:
        User: Объект пользователя, если найден, иначе None.
    """
    return User.query.get(int(user_id))


main_bp = Blueprint('main', __name__)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обрабатывает страницу авторизации.

    Если запрос POST и форма валидна, проверяет данные пользователя и выполняет вход.
    В случае успеха перенаправляет на страницу аккаунта.

    Returns:
        HTML-страница: Страница авторизации или перенаправление на аккаунт.
    """
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
    """
    Отображает страницу регистрации.

    Returns:
        HTML-страница: Форма регистрации.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@main_bp.route('/register', methods=['POST'])
def add_user():
    """
    Добавляет нового пользователя в базу данных.

    Получает данные из формы, создает объект пользователя и сохраняет его в базе данных.
    После успешной регистрации отправляет приветственное письмо.

    Returns:
        Перенаправление: На страницу входа при успехе.
        JSON-ответ: Сообщение об ошибке при неудаче.
    """
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

        send_email(
            app=current_app,
            to=new_user.email,
            subject="Добро пожаловать!",
            template="Привет, {username}! Спасибо за регистрацию на нашем сайте. Надеемся, что учеба с нами будет интересным и легким приключением.",
            username=new_user.username,
        )
        print('письмо отправлено')

        return redirect(url_for('main.login'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/')
def index():
    """
    Главная страница приложения.

    Returns:
        Перенаправление: На страницу лендинга.
    """
    return redirect(url_for('main.landing'))

@main_bp.route('/landing')
def landing():
    """
    Отображает страницу лендинга.

    Returns:
        HTML-страница: Лендинг.
    """
    return render_template('landing.html')

@main_bp.route('/textbook')
def textbook():
    """
    Отображает страницу учебника.

    Returns:
        HTML-страница: Учебник.
    """
    return render_template('textbook.html')

@main_bp.route('/tasks')
def show_tasks():
    """
    Отображает список задач.

    Returns:
        HTML-страница: Список задач.
    """
    return render_template('tasks.html', tasks=TASKS)

@main_bp.route('/tasks/<int:task_id>')
def task_view(task_id):
    """
    Отображает детали конкретной задачи.

    Args:
        task_id (int): Идентификатор задачи.

    Returns:
        HTML-страница: Детали задачи.
    """
    # ищем задачу во всех уровнях сложности
    for lvl in TASKS.values():
        for t in lvl:
            if t['id'] == task_id:
                return render_template('task_view.html', task=t)

@main_bp.route('/support', methods=['GET'])
def support():
    """
    Отображает страницу поддержки.

    Returns:
        HTML-страница: Поддержка.
    """
    return render_template('support.html')


@main_bp.route('/user-agreement', methods=['GET'])
def user_agreement():
    """
    Отображает пользовательское соглашение.

    Returns:
        HTML-страница: Пользовательское соглашение.
    """
    return render_template('user_agreement.html')

ai_chat_bp = Blueprint('ai_chat', __name__)


@ai_chat_bp.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    """
    Обрабатывает страницу AI-чата.

    Для GET-запросов отображает интерфейс чата.
    Для POST-запросов вызывает функцию обработки запроса к AI.

    Returns:
        HTML-страница: Интерфейс чата.
        JSON-ответ: Результаты обработки запроса.
    """
    if request.method == 'POST':
        return handle_ai_chat(request)
    return render_template('ai_chat.html')


@main_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Отображает и обновляет профиль пользователя.

    Если форма валидна, обновляет данные пользователя в базе данных.

    Returns:
        HTML-страница: Профиль пользователя.
    """
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
    """
    Выполняет выход пользователя.

    Returns:
        Перенаправление: На главную страницу.
    """
    logout_user()
    return redirect(url_for('main.index'))


@main_bp.route('/my-courses')
def my_courses():
    """
    Отображает страницу курсов пользователя.

    Returns:
        HTML-страница: Курсы пользователя.
    """
    return render_template('courses.html', form=form)