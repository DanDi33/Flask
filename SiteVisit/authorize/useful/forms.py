from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    name = StringField("Имя", validators=[Length(min=4, max=25, message="Пароль должен содержать от 4 до 25 "
                                                                        "символов")])
    psw = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100,
                                                                     message="Пароль должен содержать от 4 до 100 "
                                                                             "символов")])
    remember = BooleanField("Запомни меня ", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[Length(min=4, max=25, message="Имя должно содержать от 4 до 25 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100,
                                                                       message="Пароль должен содержать от 4 до 100 "
                                                                               "символов")])
    psw2 = PasswordField("Повторите пароль: ", validators=[DataRequired(), EqualTo('psw', message="Пароли должны совпадать")])
    submit = SubmitField("Зарегистировать")
