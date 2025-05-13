from flask_mail import Message, Mail

def send_email(app, to, subject, template, **kwargs):
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