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
