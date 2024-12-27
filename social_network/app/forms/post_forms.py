from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    post = TextAreaField('Напишите что-нибудь...', validators=[
        DataRequired(),
        Length(min=1, max=140)
    ])
    submit = SubmitField('Опубликовать')
