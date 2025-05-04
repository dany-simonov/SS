from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from social_network.app.tasks_data import TASKS
from social_network.app.ai_chat import handle_ai_chat

main_bp = Blueprint('main', __name__)

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

# @main_bp.route('/task_view')
# def task_view():
#     task_title = request.args.get('title')
#     return render_template('task_view.html', task_title=task_title)
@main_bp.route('/tasks/<int:task_id>')
def task_view(task_id):
    # ищем задачу во всех уровнях сложности
    for lvl in TASKS.values():
        for t in lvl:
            if t['id'] == task_id:
                return render_template('task_view.html', task=t)
    abort(404)

@main_bp.route('/support', methods=['GET'])
def support():
    return render_template('support.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Логика регистрации
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Логика входа
    return render_template('login.html')

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