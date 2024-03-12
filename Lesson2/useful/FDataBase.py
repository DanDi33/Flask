import math
import re
import sqlite3
import time
import datetime

from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM Mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Error get data from DataBase")
        return []

    def addPost(self, site, author, title, description, url, urlToImage):
        if author is None:
            author = ""
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM posts WHERE url LIKE ?", (url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с данным url уже есть!")
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES (NULL,?,?,?,?,?,?,?)", (site, author, title, description, url,
                                                                                 urlToImage, tm))
            self.__db.commit()
        except Exception as e:
            print(f"Error adding post. {e}")
            return False
        return True

    def getPostAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, description, url, urlToImage, time FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                res_arr = []
                for el in res:
                    timestamp = el['time']
                    dt_object = datetime.datetime.fromtimestamp(timestamp)
                    res_arr.append({'id': el['id'], 'title': el['title'], 'description': el['description'],
                                    'url': el['url'], 'urlToImage': el['urlToImage'],
                                    'time': dt_object.strftime("%H:%M:%S, %d.%m.%Y")})
                # print(res_arr)
                return res_arr
        except sqlite3.Error as e:
            print(f"Ошибка при получении постов из БД. {e}")
        return []

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT url FROM posts WHERE id LIKE ? LIMIT 1", (alias,))
            res = self.__cur.fetchone()
            # print(res)
            if res:
                print(res)
                #         base = url_for('static', filename="img")
                #         text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                # "\\g<tag>"+base+"/\\g<url>>",
                # res['text'])
                return res
        except sqlite3.Error as e:
            print(f"Ошибка при получении поста из БД. {e}")
        return False
