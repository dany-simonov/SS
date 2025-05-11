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