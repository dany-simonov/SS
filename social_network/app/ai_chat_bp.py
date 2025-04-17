from flask import Blueprint, render_template, request, jsonify

# Создание Blueprint для AI-чата
ai_chat_bp = Blueprint('ai_chat_bp', __name__)

@ai_chat_bp.route('/ai-chat', methods=['GET', 'POST'])
def ai_chat():
    if request.method == 'POST':
        # Обработка POST-запроса
        data = request.get_json()
        user_message = data.get('message')
        return jsonify({'response': f'AI: Вы сказали "{user_message}"'})
    return render_template('ai_chat.html')