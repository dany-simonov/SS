from flask import url_for
from social_network.app.models import User


def test_home_page(client):
    """Тест для главной страницы"""
    response = client.get('/')
    assert response.status_code == 302


def test_landing_page(client):
    """Тест для landing"""
    response = client.get('/landing')
    assert response.status_code == 200
    print(response.data)


def test_login_page(client):
    """Тест для страницы логина"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_register_page(client):
    """Тест для страницы регистрации"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_user(client):
    """Тест регистрации нового пользователя"""
    response = client.post('/register', data={
        'username': 'test user x',
        'email': 'testuserx@example.com',
        'password': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b"Sign In" in response.data


def test_login_user(client, new_user):
    """Тест входа пользователя"""
    response = client.post(
        url_for("main.login"),
        content_type='multipart/form-data',
        data={
            'username': 'test',
            'password': 'password123'
        },
        follow_redirects=True
    )

    print(response.data)
    assert response.status_code == 200

    assert b"Account" in response.data


def test_logout_user(client, new_user):
    """Тест выхода пользователя"""
    response = client.post(url_for('main.login'), data={
        'username': 'test',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account' in response.data

    response = client.get(url_for('main.logout'), follow_redirects=True)
    assert response.status_code == 200