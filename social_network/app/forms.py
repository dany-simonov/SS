from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class LoginForm(FlaskForm):
  """
  Форма для авторизации пользователя.

  Поля:
      username (StringField): Имя пользователя. Обязательное поле.
      password (PasswordField): Пароль. Обязательное поле.
      remember_me (BooleanField): Флажок "Запомнить меня".
      submit (SubmitField): Кнопка отправки формы.
  """
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
  """
  Форма для регистрации нового пользователя.

  Поля:
      username (StringField): Имя пользователя. Обязательное поле, длина от 4 до 80 символов.
      email (StringField): Электронная почта. Обязательное поле, должно быть валидным email-адресом.
      password (PasswordField): Пароль. Обязательное поле, минимальная длина — 6 символов.
      submit (SubmitField): Кнопка отправки формы.
  """
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
  submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
  """
  Форма для редактирования профиля пользователя.

  Поля:
      username (StringField): Имя пользователя. Обязательное поле.
      email (StringField): Электронная почта. Обязательное поле, должно быть валидным email-адресом.
      first_name (StringField): Имя. Необязательное поле.
      last_name (StringField): Фамилия. Необязательное поле.
      age (StringField): Возраст. Необязательное поле.
      submit (SubmitField): Кнопка отправки формы.
    """
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  first_name = StringField('First Name', validators=[Optional()])
  last_name = StringField('Last Name', validators=[Optional()])
  age = StringField('Age', validators=[Optional()])
  submit = SubmitField('Save Changes')
