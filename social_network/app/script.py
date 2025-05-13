from flask import Blueprint

from social_network.app import db
from social_network.app.models import Courses
from social_network.app import tasks_data


import_tasks = Blueprint('import_tasks', __name__)

@import_tasks.cli.command("add-task")
def add_task():
    """Берет задачи из файла tasks_data и загружает в бд"""

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
    db.session.commit()
    print("Задача успешно добавлена!")
