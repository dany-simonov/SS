from flask import Blueprint
from .quizzes_bp import init_quiz_routes

quizzes_bp = Blueprint(
    'quizzes_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/quizzes/static',
    url_prefix='/quizzes'
)

# Регистрация маршрутов
init_quiz_routes(quizzes_bp)
