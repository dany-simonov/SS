import pytest
from social_network.app.forms import LoginForm, RegistrationForm, EditProfileForm


@pytest.mark.usefixtures("app")
def test_login_form_valid(app):
    """Тест валидации входа"""
    with app.app_context():
        form = LoginForm(username="testuser", password="password123")
    assert form.validate() is True


@pytest.mark.usefixtures("app")
def test_registration_form_valid(app):
    """Тест валидации регистрации"""
    form = RegistrationForm(
        username="newuser",
        email="newuser@example.com",
        password="password123",
    )
    assert form.validate() is True


@pytest.mark.usefixtures("app")
def test_registration_form_invalid_password(app):
    """Тест невалидной регистрации"""
    form = RegistrationForm(
        username="newuser",
        email="newuser@example.com",
        password="pas",
    )
    assert form.validate() is False


@pytest.mark.usefixtures("app")
def test_registration_form_invalid_email(app):
    """Тест невалидной регистрации"""
    form = RegistrationForm(
        username="newuser",
        email="newuserexample.com",
        password="password",
    )
    assert form.validate() is False


@pytest.mark.usefixtures("app")
def test_registration_form_user_is_already_registered(app):
    """Тестирование невалидной формы регистрации."""
    form = RegistrationForm(
        username="User",
        email="newusere@xample.com",
        password="pas",
    )
    assert form.validate() is False


def test_valid_form(form):
    """Тестирование корректного заполнения формы."""
    form.username.data = "testuser"
    form.email.data = "test@example.com"
    form.first_name.data = "Test"
    form.last_name.data = "User"
    form.age.data = "25"

    assert form.validate() is True
    assert form.username.errors == []
    assert form.email.errors == []


def test_missing_required_fields(form):
    """Тестирование формы с отсутствующими обязательными полями."""
    form.username.data = ""
    form.email.data = ""

    assert form.validate() is False
    assert "This field is required." in form.username.errors
    assert "This field is required." in form.email.errors


def test_invalid_email(form):
    """Тестирование формы с некорректным email."""
    form.username.data = "testuser"
    form.email.data = "invalid-email"

    assert form.validate() is False
    assert "Invalid email address." in form.email.errors


def test_optional_fields(form):
    """Тестирование формы с необязательными полями."""
    form.username.data = "testuser"
    form.email.data = "test@example.com"
    form.first_name.data = ""
    form.last_name.data = ""
    form.age.data = ""

    assert form.validate() is True
    assert form.first_name.errors == []
    assert form.last_name.errors == []
    assert form.age.errors == []