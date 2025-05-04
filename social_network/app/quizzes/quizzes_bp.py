import json
import random
import os
from flask import Blueprint, render_template, request, session, jsonify

quizzes_bp = Blueprint(
    'quizzes_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/quizzes'
)

# Путь к файлу с вопросами
QUESTIONS_PATH = os.path.join(
    os.path.dirname(__file__),
    'questions.json'
)

# Загружаем все вопросы в память один раз
with open(QUESTIONS_PATH, encoding='utf-8') as f:
    QUIZZES = json.load(f)


@quizzes_bp.route('/', methods=['GET'])
def choose():
    """
    Страница выбора темы и уровня сложности квиза.
    """
    return render_template('quizzes.html')


@quizzes_bp.route('/start', methods=['POST'])
def start():
    """
    Генерирует 5 случайных вопросов заданной темы и сложности,
    сохраняет их в сессии и показывает страницу с квизом.
    """
    topic = request.form.get('topic')
    level = request.form.get('level')

    # Берём список вопросов для выбранной темы и уровня
    pool = QUIZZES.get(topic, {}).get(level, [])
    selected = random.sample(pool, min(5, len(pool)))

    # Сохраняем выбранные вопросы в сессии
    session['quiz_questions'] = selected

    return render_template(
        'quiz.html',
        questions=selected,
        topic=topic,
        level=level
    )


@quizzes_bp.route('/answer', methods=['POST'])
def answer():
    """
    Проверяет ответ пользователя и возвращает результат в JSON.
    """
    data = request.get_json()
    question_id = data.get('id')
    user_answer = data.get('answer', '').strip().lower()

    quiz_questions = session.get('quiz_questions', [])

    # Ищем вопрос по ID
    question = next((q for q in quiz_questions if q.get('id') == question_id), None)

    if not question:
        return jsonify({
            "correct": False,
            "correct_answer": "неизвестно",
            "explanation": "Вопрос не найден."
        }), 404

    correct_answer = question.get('answer', '').strip().lower()
    explanation = question.get('explanation', '')

    return jsonify({
        "correct": user_answer == correct_answer,
        "correct_answer": question.get('answer', ''),
        "explanation": explanation
    })
