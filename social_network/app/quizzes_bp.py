import json
import random
import os
from flask import Blueprint, render_template, request, session, jsonify

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), 'questions.json')
with open(QUESTIONS_PATH, encoding='utf-8') as f:
    QUIZZES = json.load(f)
    
quizzes_bp = Blueprint('quizzes_bp', __name__, url_prefix='/quizzes')

@quizzes_bp.route('/choose', methods=['GET'])
def choose():
    return render_template('quizzes.html')

@quizzes_bp.route('/start', methods=['POST'])
def start():
    topic = request.form.get('topic')
    level = request.form.get('level')
    pool = QUIZZES.get(topic, {}).get(level, [])
    selected = random.sample(pool, min(5, len(pool)))
    session['quiz_questions'] = selected
    return render_template('quiz.html', questions=selected, topic=topic, level=level)

@quizzes_bp.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    qid, ua = data.get('id'), data.get('answer','').strip().lower()
    qs = session.get('quiz_questions', [])
    q = next((x for x in qs if x['id']==qid), None)
    if not q:
        return jsonify(correct=False, correct_answer="?", explanation="Вопрос не найден"),404
    correct = q['answer'].strip().lower()
    return jsonify(
      correct=ua==correct,
      correct_answer=q['answer'],
      explanation=q.get('explanation','')
    )

@quizzes_bp.route('/results', methods=['GET'])
def results():
    return render_template('results.html')
