import logging
import os
import tempfile
import uuid
import pytest
from social_network.app import create_app
from social_network.app.forms import EditProfileForm
from social_network.app.models import db, User, Courses

unique_email = f"test-{uuid.uuid4()}@example.com"

@pytest.fixture
def app():
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, "test.db")

    app = create_app(conf='social_network.tests.config')
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{test_db_path}",
        "SERVER_NAME": "localhost",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.rollback()
        db.drop_all()

    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    os.rmdir(temp_dir)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def new_user(app):
    """Создание пользователя для тестов"""
    user = User(
        username="test",
        email='testussrr@mail.com',
        first_name="Test",
        last_name="User",
        age=25,
    )
    user.set_password("password123")
    with app.app_context():
        db.session.expire_on_commit = False
        db.session.add(user)
        db.session.commit()

        yield db.session.get(User, user.id)


@pytest.fixture
def new_course(app):
    """Создание курса для тестов"""
    course = Courses(
        course_name="Python Basics",
        difficulty=1,
        title="Introduction to Python",
        description="Learn the basics of Python programming.",
        input_example="print('Hello, world!')",
        output_example="Hello, world!"
    )
    with app.app_context():
        db.session.expire_on_commit = False
        db.session.add(course)
        db.session.commit()

        yield db.session.get(Courses, course.id)