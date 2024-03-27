from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TelField, TextAreaField, URLField
from wtforms.validators import Email, DataRequired, Length, EqualTo, URL


class ProfileForm(FlaskForm):
    logos = [("None", "Выберите лого"),
             ("vk", "vk"),
             ("twitter", "twitter"),
             ("instagram", "instagram"),
             ("facebook", "facebook"),
             ("youtube", "youtube"),
             ("linkedin", "linkedin"),
             ("behance", "behance"),
             ("dribbble", "dribbble"),
             ("whatsapp", "whatsapp"),
             ("wechat", "wechat"),
             ("wordpress", "wordpress"),
             ("twitch", "twitch"),
             ("yahoo", "yahoo"),
             ]
    name = StringField("Имя", validators=[Length(min=2, max=25, message="Имя должно содержать от 2 до 25 "
                                                                        "символов")], description="Ваше имя")
    surname = StringField("Фамилия", validators=[Length(min=2, max=40, message="Фамилия должна содержать от 2 до 25 "
                                                                               "символов")], description="Ваша фамилия")
    avatar = FileField()
    phone = TelField("Мобильный номер", validators=[Length(min=10, max=10, message="Номер телефона содержит 10 цифр")],
                     description="Введите номер телефона")
    profession = StringField("Профессия", validators=[Length(min=4, max=40, message="Профессия должна содержать от 4 "
                                                                                    "до 25 символов")],
                             description="Ваша профессия")
    about = TextAreaField("О себе", validators=[Length(min=0, max=200, message="Поле 'О себе' должно содержать "
                                                                               "до 200 символов")],
                          description="Здесь Вы можете написать о себе, своих скиллам, хобби, достижениях")
    logo1 = SelectField("Logo", choices=logos, default=None)
    logo2 = SelectField("Logo", choices=logos, default=None)
    logo3 = SelectField("Logo", choices=logos, default=None)
    logo4 = SelectField("Logo", choices=logos, default=None)
    logo5 = SelectField("Logo", choices=logos, default=None)
    logo6 = SelectField("Logo", choices=logos, default=None)
    url1 = URLField("URL",
                    description="Введите ссылку на Вашу страницу")
    url2 = URLField("URL",
                    description="Введите ссылку на Вашу страницу")
    url3 = URLField("URL",
                    description="Введите ссылку на Вашу страницу")
    url4 = URLField("URL",
                    description="Введите ссылку на Вашу страницу")
    url5 = URLField("URL",
                    description="Введите ссылку на Вашу страницу")
    url6 = URLField("URL",
                    description="Введите ссылку на Вашу страницу")
    submit = SubmitField("Сохранить")

# validators=[URL(message="Enter Valid URL Please.")],
