import os
from PIL import Image

import flask
from flask import Blueprint, render_template, redirect, url_for, flash, session, g, json
import sqlite3

from werkzeug.utils import secure_filename
from SiteVisit.adminPanel.useful.forms import ProfileForm

admin = Blueprint('adminPanel', __name__, template_folder='templates', static_folder='static')
menu = [{"url": "adminPanel.index", "title": "Удалить профиль"},
        {"url": "authorize.logout", "title": "Выйти"}]

db = None


@admin.before_request
def before_request():
    # Подключение к базе. Присваиваем db link_db
    global db
    db = g.get("link_db")


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route("/", methods=["POST", "GET"])
@admin.route("/profile", methods=["POST", "GET"])
def index():
    social_in = []

    if not isLogged():
        return redirect(url_for('authorize.login'))

    profile = select_user(session['name'])

    if profile is None:
        print(f"Профиль {session['name']} - не найден (adminPanel/admin.py def index).")
        return redirect(url_for('authorize.login'))

    social_out = json.loads(profile['social'])
    form = ProfileForm()

    if form.validate_on_submit():
        for i in range(6):
            if form[f'logo{i + 1}'].data != 'None' and form[f'url{i + 1}'].data != 'None':
                social_in.append({'log_num': form[f'logo{i + 1}'].name, 'name': form[f'logo{i + 1}'].data,
                                  'name_url': form[f'url{i + 1}'].name, 'url': form[f'url{i + 1}'].data})

        if form.avatar.data:
            image = form.avatar.data

            # Создаю имя файла вида: "логин" + ".расширение исходного файла"
            last_part = image.filename.split('.')[-1]
            filename = secure_filename(f"{profile['user_name']}.{last_part}")

            # Создаю директорию "uploads", если ее нет
            os.makedirs(flask.current_app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Сохраняю файл с новым именем в директории "uploads"
            image.save(os.path.join(flask.current_app.config['UPLOAD_FOLDER'], filename))

            # Обрезаю аватарку по наименьшей стороне до квадрата
            im = Image.open(os.path.join(flask.current_app.config['UPLOAD_FOLDER'], filename))
            im_new = crop_max_square(im)
            im_new.save(os.path.join(flask.current_app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = profile['avatar']
            if not filename:
                filename = ''
        if db:
            try:
                cur = db.cursor()
                cur.execute(f"UPDATE profiles SET 'name' = ?, "
                            f"'surname' = ?, "
                            f"'avatar' = ?, "
                            f"'phone' = ?, "
                            f"'profession' = ?, "
                            f"'about' = ?, "
                            f"'social' = ?, "
                            f"'type_profile' = ? "
                            f"WHERE id LIKE ?;", (form.name.data,
                                                  form.surname.data,
                                                  filename,
                                                  form.phone.data,
                                                  form.profession.data,
                                                  form.about.data,
                                                  json.dumps(social_in),
                                                  int(form.type_profile.data),
                                                  session['id']))
                db.commit()
                return redirect(url_for('adminPanel.index'))
            except sqlite3.Error as e:
                flash("Ошибка при добавлении в БД", category="error")
                print("Ошибка добавления в БД." + str(e) + ". (adminPanel/admin.py def index).")

    return render_template("adminPanel/profile.html", title="Главная", menu=menu,
                           profile=profile, form=form, social=social_out)


def select_user(user_name):
    # Функция из БД возвращает профиль по логину(user_name)
    # При обращении к функции, возьми name из session (session['name])
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT * FROM profiles WHERE user_name = "{user_name}" LIMIT 1')
            profile = cur.fetchall()[0]
            if not profile:
                print(f"Профиль {user_name} - не найден (adminPanel/admin.py def select_user).")
                return None
        except sqlite3.Error as e:
            print(f'Ошибка при запросе к БД -  (adminPanel/admin.py def select_user). {e}')
            return None
        print(f"Данные профиля {user_name} успешно выгружены. (adminPanel/admin.py def select_user).")
        return profile
    print(f"Ошибка подключения к БД. db - False (adminPanel/admin.py def select_user).")
    return None


@admin.route("/delete_current_user", methods=["GET", "POST"])
def delete_current_user():
    if not isLogged():
        return redirect(url_for('authorize.login'))

    profile = select_user(session['name'])

    if profile is None:
        print(f"Профиль {session['name']} - не найден. (adminPanel/admin.py def delete_current_user).")
        return redirect(url_for('authorize.login'))

    avatar_file = f"uploads/{profile['avatar']}"

    if os.path.isfile(avatar_file):
        os.remove(avatar_file)
        print("Файл (%s) успешно удален" % profile['avatar'])
    else:
        print("Файл (%s) не найден" % profile['avatar'])
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"DELETE FROM profiles WHERE user_name = '{session['name']}';")
            cur.execute(f"DELETE FROM users WHERE name = '{session['name']}';")
            db.commit()
            flash(f"Пользователь {session['name']} успешно удален", category="success")
            print(f"Пользователь {session['name']} удален из БД. (adminPanel/admin.py def delete_current_user).")
            return redirect(url_for('authorize.logout'))

        except sqlite3.Error as e:
            flash(f"Ошибка при удалении пользователя {session['name']} из БД", category="error")
            print(f"Ошибка при удалении пользователя {session['name']} из БД." + str(e) + ". (adminPanel/admin.py "
                                                                                          "def delete_current_user).")
            return redirect(url_for('adminPanel.index'))
    else:
        flash(f"Ошибка соединения с БД", category="error")
        print(f"Ошибка соединения с БД. (adminPanel/admin.py def delete_current_user).")
        return redirect(url_for('adminPanel.index'))


@admin.route("/userava")
def userava():
    profile = select_user(session['name'])
    img = None
    if not profile["avatar"]:
        try:
            with flask.current_app.open_resource(flask.current_app.root_path +
                                                 url_for('static', filename='img/profile-image.jpg'),
                                                 "rb") as file:
                img = file.read()
        except FileNotFoundError as e:
            print(f"Дефолтный аватар не найден. (adminPanel/admin.py  def userava) {e}")
    else:
        try:
            with flask.current_app.open_resource(flask.current_app.root_path + "/uploads/" + profile["avatar"],
                                                 "rb") as file:
                img = file.read()
        except FileNotFoundError as e:
            print(f"Файл аватара не найден. (adminPanel/admin.py  def userava) {e}")
            try:
                with flask.current_app.open_resource(flask.current_app.root_path +
                                                     url_for('static', filename='img/profile-image.jpg'),
                                                     "rb") as file:
                    img = file.read()
                    print(f"Успешно использован дефолтный аватар. (adminPanel/admin.py  def userava)")
            except FileNotFoundError as e:
                print(f"Дефолтный аватар не найден. (adminPanel/admin.py  def userava) {e}")
    return img


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    """
    Функция принимает картинку и возвращает квадратную картинку.
    """
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def isLogged():
    print(session)
    return True if session.get('name') else False
