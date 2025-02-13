from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import g4f

providers = [
    g4f.Provider.You
]
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'StudySphere_2024_SuperSecretKey_789@#$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Здесь будут модели (можно потом вынести в models.py)
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

@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/landing')
def landing():
    return render_template('landing.html')

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

@app.route('/ai-chat', methods=['GET', 'POST'])
def ai_chat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({'success': False, 'message': 'Пожалуйста, введите сообщение.'})

        system_prompt = "Ты - помощник StudySphere, образовательной платформы. Твоя задача помогать студентам с учебными вопросами."

        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                stream=False
            )
            
            if response:
                return jsonify({'success': True, 'response': response})
                
        except Exception as e:
            print(f"Ошибка чата: {str(e)}")
            
        return jsonify({'success': False, 'message': 'Попробуйте еще раз через минуту'})

    return render_template('ai_chat.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)