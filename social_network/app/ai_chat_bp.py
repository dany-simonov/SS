# from flask import Blueprint, render_template, request, jsonify

# # Создание Blueprint для AI-чата
# ai_chat_bp = Blueprint('ai_chat_bp', __name__)

# @ai_chat_bp.route('/ai-chat', methods=['GET', 'POST'])
# def ai_chat():
#     if request.method == 'POST':
#         # Обработка POST-запроса
#         data = request.get_json()
#         user_message = data.get('message')
#         return jsonify({'response': f'AI: Вы сказали "{user_message}"'})
#     return render_template('ai_chat.html')
from flask import Blueprint, render_template, request, jsonify
from .ai_chat import handle_ai_chat

ai_chat_bp = Blueprint(
    'ai_chat_bp',
    __name__,
    url_prefix='/ai-chat',
    template_folder='templates',
    static_folder='static'
)

@ai_chat_bp.route('/', methods=['GET', 'POST'])
def ai_chat():
    if request.method == 'POST':
        return handle_ai_chat(request)
    return render_template('ai_chat.html')