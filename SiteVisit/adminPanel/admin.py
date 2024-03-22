import math
import time
from flask import Blueprint, render_template, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from SiteVisit.adminPanel.useful.forms import ProfileForm

admin = Blueprint('adminPanel', __name__, template_folder='templates', static_folder='static')
menu = [{"url": ".index", "title": "Панель"}, {"url": "authorize.logout", "title": "Выйти"}]
logos = [{"name": "vk"},
         {"name": "twitter"},
         {"name": "instagram"},
         {"name": "facebook"},
         {"name": "youtube"},
         {"name": "linkedin"},
         {"name": "behance"},
         {"name": "dribbble"},
         {"name": "whatsapp"},
         {"name": "wechat"},
         {"name": "wordpress"},
         {"name": "twitch"},
         {"name": "yahoo"},
         ]

db = None


@admin.before_request
def before_request():
    # Подключение к базе
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
    print(session)
    if not isLogged():
        return redirect(url_for('authorize.login'))
    try:
        cur = db.cursor()
        cur.execute(f'SELECT * FROM profiles WHERE user_name = "{session['name']}" LIMIT 1')
        profile = cur.fetchall()[0]
        if not profile:
            print(f"Профиль {session['name']} - не найден")
            return redirect(url_for('authorize.login'))
    except sqlite3.Error as e:
        print(f'Ошибка авторизации - adminPanel.index. {e}')
        return redirect(url_for('authorize.login'))
    form = ProfileForm()
    if form.validate_on_submit():
        if profile:
            session['name'] = form.name.data
            session['surname'] = form.surname.data

    return render_template("adminPanel/profile.html", title="Главная", menu=menu,
                           profile=profile, form=form, logos=logos)


def isLogged():
    return True if session.get('name') else False
