import os
import sqlite3
from flask import Flask, render_template, g, abort, make_response, url_for, json
from useful.FDataBase import FDataBase
from authorize.login import user
from adminPanel.admin import admin

app = Flask(__name__)
app.config["SECRET_KEY"] = "wewrtrtey1223345dfgdf"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_FOLDER'] = 'uploads'


app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(admin, url_prefix="/admin")

dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    conn = sqlite3.connect('site_visit_DB.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


def create_db():
    db = connect_db()
    with app.open_resource("sql_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.route('/userava')
def userava():
    try:
        with app.open_resource(app.root_path + url_for('static', filename='img/profile-image.jpg'), "rb") as file:
            img = file.read()
    except FileNotFoundError as e:
        print(f"Дефолтный аватар не найден. {e}")
    if not img:
        return ""
    answer = make_response(img)
    answer.headers["Content-Type"] = "image/png"
    return answer


@app.route("/")
def index():
    if not os.path.exists("lesson2_DB.db"):
        create_db()
    default_res = dict()
    (default_res['name'], default_res['surname'], default_res['email'],
     default_res['phone'], default_res['profession'], default_res['about'],
     default_res['social']) = ("Ethan", "Rivers", "evan@google.com", 79009007777, "UI / UX Designer",
                               "Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam atque, "
                               "ipsam a amet laboriosam eligendi.", [{"name": "dribbble", "url": "https"
                                                                                                 "://dribbble.com/"},
                                                                     {"name": "instagram", "url": "https"
                                                                                                  "://instagram.com/"},
                                                                     {"name": "twitter", "url": "https"
                                                                                                "://x.com/"},
                                                                     {"name": "linkedin", "url": "https://careers"
                                                                                                 ".linkedin.cn/"},
                                                                     {"name": "facebook",
                                                                      "url": "https://facebook.com/"},
                                                                     {"name": "behance",
                                                                      "url": "https://www.behance.net/"}])
    return render_template("profile.html", res=default_res)


@app.route("/<alias>", methods=["GET", "POST"])
def showpost(alias):
    res = dict()
    (res['user_name'], res['name'], res['surname'], res['email'],
     res['phone'], res['profession'], res['about'], res['social'], res['avatar']) = dbase.get_profile(alias)
    # image_binary = read_image(res['avatar'])
    # response = make_response(image_binary)
    # response.headers.set('Content-Type', 'image/jpeg')
    if not res['user_name']:
        abort(404)
    if not res['name']:
        res['name'] = 'Your'
    if not res['surname']:
        res['surname'] = 'name'
    if not res['email']:
        res['email'] = '#'
    if not res['phone']:
        res['phone'] = '#'
    if not res['profession']:
        res['profession'] = 'your profession'
    if not res['about']:
        res['about'] = 'tell about your skills'
    return render_template("profile.html", res=res, title=alias)


@app.errorhandler(404)
def pageNotFounded(error):
    return render_template("page404.html", title="Страница не найдена")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


if __name__ == "__main__":
    # create_db()
    app.run(debug=True)
