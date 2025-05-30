from flask_mail import Message, Mail

def send_email(app, to, subject, template, **kwargs):
    """
    Отправляет электронное письмо с использованием Flask-Mail.

    Аргументы:
        app (Flask): Экземпляр приложения Flask, необходимый для работы в контексте приложения.
        to (str): Email-адрес получателя письма.
        subject (str): Тема письма.
        template (str): Шаблон текста письма. Может содержать заполнители для форматирования.
        **kwargs: Дополнительные параметры, которые будут подставлены в шаблон письма.

    Описание:
        Функция создает и отправляет электронное письмо через Flask-Mail. Она использует контекст
        приложения Flask для корректной работы с конфигурацией и отправкой письма.

    Пример использования:
        send_email(
            app=my_flask_app,
            to="user@example.com",
            subject="Добро пожаловать!",
            template="Привет, {username}! Спасибо за регистрацию.",
            username="Иван"
        )

    Важно:
        Убедитесь, что в конфигурации приложения настроены параметры Flask-Mail, такие как
        MAIL_DEFAULT_SENDER и MAIL_SERVER.
    """
    with app.app_context():
        from flask_mail import Message, Mail
        msg = Message(
            subject=subject,
            recipients=[to],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        msg.body = template.format(**kwargs)
        mail = Mail(app)
        mail.send(msg)