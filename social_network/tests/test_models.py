import uuid

from sqlalchemy.testing import db

from social_network.app.models import Courses
from social_network.tests.conftest import unique_email


def test_user_creation(new_user):
    """Тестирование создания пользователя."""
    assert new_user.username == "test"
    assert new_user.email == 'testussrr@mail.com'
    assert new_user.first_name == "Test"
    assert new_user.last_name == "User"
    assert new_user.age == 25


def test_set_password(new_user):
    """Тестирование метода set_password."""
    assert new_user.check_password("password123") is True
    assert new_user.check_password("wrongpassword") is False


def test_course_creation(new_course):
    """Тестирование создания курса."""
    assert new_course.course_name == "Python Basics"
    assert new_course.difficulty == 1
    assert new_course.title == "Introduction to Python"
    assert new_course.description == "Learn the basics of Python programming."
    assert new_course.input_example == "print('Hello, world!')"
    assert new_course.output_example == "Hello, world!"