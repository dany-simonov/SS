"""
Модуль для работы с AI-чатом.

Этот модуль предоставляет Blueprint для обработки запросов, связанных с AI-чатом.
Он включает маршрут для отображения интерфейса чата и обработки POST-запросов
для взаимодействия с AI.

Blueprint:
    ai_chat_bp: Blueprint для маршрутов, связанных с AI-чатом.

Routes:
    /: Основной маршрут для отображения интерфейса чата и обработки запросов.
"""
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
    """
    Обрабатывает запросы к AI-чату.

    - Для GET-запросов отображается страница чата (`ai_chat.html`).
    - Для POST-запросов вызывается функция `handle_ai_chat`, которая обрабатывает
      входящие данные и возвращает JSON-ответ с результатами.

    Methods:
        GET: Отображает шаблон `ai_chat.html` для взаимодействия с пользователем.
        POST: Принимает JSON-данные, передает их в `handle_ai_chat` и возвращает ответ.

    Returns:
        GET: HTML-страница с интерфейсом чата.
        POST: JSON-ответ с результатами обработки запроса.
    """
    if request.method == 'POST':
        return handle_ai_chat(request)
    return render_template('ai_chat.html')