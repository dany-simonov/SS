from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import g4f
from enhanced_generation import EnhancedGeneration
import asyncio
import re

#python social_network/app/app.py

text_providers = [
    g4f.Provider.ChatGLM,
    g4f.Provider.Free2GPT,
    g4f.Provider.GizAI
]

image_providers = [
    g4f.Provider.ImageLabs
]

g4f.debug.logging = True
g4f.check_version = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'StudySphere_2024_SuperSecretKey_789@#$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Маршруты
@app.route('/')
def index():
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/textbook')
def textbook():
    return render_template('textbook.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

# @app.route('/task/<int:task_id>')
# def task_view(task_id):
#     return render_template('task_view.html', task_id=task_id)

@app.route('/task_view')
def task_view():
    task_title = request.args.get('title')
    return render_template('task_view.html', task_title=task_title)

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Пользователь уже существует'})
    
    user = User(username=data['username'], phone=data['phone'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Неверное имя пользователя или пароль'})

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def is_valid_image_url(url: str) -> bool:
    """Проверяет валидность URL изображения"""
    if not url:
        return False
    
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return any(url.lower().endswith(ext) for ext in valid_extensions)

def extract_image_url(html_response: str) -> str:
    """Извлекает URL изображения из HTML-ответа"""
    url_pattern = r'https://[^\s<>"]+?(?:jpg|jpeg|png|gif|webp)'
    matches = re.findall(url_pattern, html_response)
    return matches[0] if matches else ''

@app.route('/execute-code', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    try:
        # Создаем изолированное окружение для выполнения кода
        local_dict = {}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        
        # Получаем результат выполнения
        output = local_dict.get('result', 'Код выполнен успешно')
        return jsonify({'success': True, 'output': output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'title': task.title,
        'description': task.description,
        'initial_code': task.initial_code
    })

@app.route('/ai-chat', methods=['GET', 'POST'])
def ai_chat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message')
        selected_model = data.get('model', 'ChatGLM')
        generation_type = data.get('type', 'text')
        is_enhanced = data.get('enhanced', False)

        if not user_message:
            return jsonify({'success': False, 'message': 'Пожалуйста, введите сообщение.'})
        
        system_prompt = """Ты - дружелюбный AI-ассистент StudySphere. Твои основные задачи:
                        - Помогать с учебными вопросами по любым предметам
                        - Объяснять сложные темы простым языком  
                        - Давать практические советы по обучению
                        - Поддерживать мотивацию к учёбе
                        - Общаться в дружелюбном тоне
                        - Можешь шутить и поддерживать неформальную беседу
                        - При этом всегда оставаться полезным и информативным."""

        if generation_type == 'text':
            try:
                if is_enhanced:
                    # Используем улучшенную генерацию
                    enhanced_gen = EnhancedGeneration()
                    result = asyncio.run(enhanced_gen.get_response(user_message))
                    return jsonify(result)
                else:
                    # Обычная генерация с выбранной моделью
                    provider_map = {
                        'ChatGLM': g4f.Provider.ChatGLM,
                        'Free3GPT': g4f.Provider.Free2GPT,
                        'GizAI': g4f.Provider.GizAI
                    }
                    
                    provider = provider_map.get(selected_model)
                    print(f"Using {selected_model} provider and gpt-3.5-turbo model")

                    response = g4f.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        provider=provider,
                        timeout=120
                    )
                    
                    return jsonify({'success': True, 'response': response})
                    
            except Exception as e:
                print(f"Ошибка модели {selected_model}: {str(e)}")
                return jsonify({'success': False, 'message': f'Ошибка при использовании {selected_model}'})
        else:
            try:
                image_provider = image_providers[0]
                raw_response = g4f.ChatCompletion.create(
                    model="image-model",
                    messages=[{"role": "user", "content": user_message}],
                    provider=image_provider,
                    timeout=120
                )
                image_url = extract_image_url(raw_response)
                if image_url:
                    response = (
                        f'<div class="image-container">'
                        f'<img src="{image_url}" style="max-width: 100%; border-radius: 5px;">'
                        f'</div>'
                    )
                    return jsonify({
                        'success': True,
                        'response': response,
                        'type': 'image'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Не удалось сгенерировать изображение'
                    })
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Ошибка при генерации изображения: {str(e)}'
                })

    return render_template('ai_chat.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)