from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import TelField, TextAreaField, URLField
from wtforms.validators import Email, DataRequired, Length, EqualTo, URL


class ProfileForm(FlaskForm):
    name = StringField("Имя", validators=[Length(min=2, max=25, message="Имя должно содержать от 2 до 25 "
                                                                        "символов")], description="Ваше имя")
    surname = StringField("Фамилия", validators=[Length(min=2, max=40, message="Фамилия должна содержать от 2 до 25 "
                                                                               "символов")], description="Ваша фамилия")
    phone = TelField("Мобильный номер", validators=[Length(min=10, max=10, message="Номер телефона содержит 10 цифр")],
                     description="Введите номер телефона")
    profession = StringField("Профессия", validators=[Length(min=4, max=40, message="Профессия должна содержать от 4 "
                                                                                    "до 25 символов")],
                             description="Ваша профессия")
    about = TextAreaField("О себе", validators=[Length(min=0, max=200, message="Поле 'О себе' должно содержать "
                                                                               "до 200 символов")],
                          description="Здесь Вы можете написать о себе, своих скиллам, хобби, достижениях")
    url1 = URLField("Url", validators=[URL(message="Enter Valid URL Please.")])
    url2 = URLField("Url", validators=[URL(message="Enter Valid URL Please.")])
    url3 = URLField("Url", validators=[URL(message="Enter Valid URL Please.")])
    url4 = URLField("Url", validators=[URL(message="Enter Valid URL Please.")])
    url5 = URLField("Url", validators=[URL(message="Enter Valid URL Please.")])
    url6 = URLField("Url", validators=[URL(message="Enter Valid URL Please.")])
    submit = SubmitField("Войти")
