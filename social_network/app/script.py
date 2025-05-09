from flask import Blueprint

from social_network.app import db
from social_network.app.models import Courses
from social_network.app import tasks_data
# from social_network.app.app import app


# db.create_all()
#
# for task in tasks_data:
#     new_task = Courses(
#         id=task['id'],
#         difficulty=task['difficulty'],
#         title=task['title'],
#         description=task['description'],
#         input_example=task['input_example'],
#         output_example=task['output_example']
#     )
#     db.session.add(new_task)
#
#
# db.session.commit()


import_tasks = Blueprint('import_tasks', __name__)

# Создаем пользовательскую команду
@import_tasks.cli.command("add-task")
def add_task():
    """Добавляет новую задачу в базу данных."""

    for task in tasks_data.TASKS["hard"]:
        new_task = Courses(
            id=task['id'],
            difficulty=task['difficulty'],
            title=task['title'],
            description=task['description'],
            input_example=task['input_example'],
            output_example=task['output_example']
        )
        db.session.add(new_task)
    # db.session.add(new_task)
    db.session.commit()
    print("Задача успешно добавлена!")
