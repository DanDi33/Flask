import math
import sqlite3
import json
import time

from newsapi import NewsApiClient
from flask import Flask, render_template, g
from useful.FDataBase import FDataBase

app = Flask(__name__)

dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    conn = sqlite3.connect('lesson2_DB.db')
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


@app.route("/")
def index():
    # print(dbase.getMenu())

    get_news("cat")
    return render_template("index.html", menu=dbase.getMenu(), title="Index page", posts=dbase.getPostAnonce())


@app.route("/post/<alias>", methods=["GET", "POST"])
def showpost(alias):
    # print(dbase.getPost(alias)['url'])
    post = dbase.getPost(alias)['url']
    return render_template("showpost.html", menu=dbase.getMenu(), title="Showpost page", post=post)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


def get_news(keyword):
    apiKey = "9b48fe6447fe4d0383f50e30af3198b9"
    try:
        newsapi = NewsApiClient(apiKey)
        news = newsapi.get_everything(q=keyword, language='ru', page_size=15)
    except Exception as e:
        news = {}
        print(f'Ошибка запроса новостей. {e}')
    news_articles = news['articles']
    print(news_articles[0])
    # with open("./news.js", "w", encoding='utf8') as outfile:
    #     json.dump(news_articles, outfile, ensure_ascii=False)
    try:
        for i, value in enumerate(news_articles):
            res = dbase.addPost(value['source']['name'], value['author'], value['title'], value['description'],
                                value['url'],
                                value['urlToImage'])
            print(f"Запись {i} добавлена в БД? {res}")
            # print(f"{i}:{value}")
            print(f"site:{value['source']['name']}")
            print(f"author:{value['author']}")
            print(f"title:{value['title']}")
            print(f"description:{value['description']}")
            print(f"url:{value['url']}")
            print(f"urlToImage:{value['urlToImage']}")
    except Exception as e:
        print(f'Ошибка записи новости в БД. {e}')
    return "done"


if __name__ == "__main__":
    create_db()
    app.run(debug=True)
