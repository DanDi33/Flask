import sqlite3

from flask import json


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_profile(self, alias):
        try:
            self.__cur.execute(f"SELECT * FROM profiles WHERE user_name LIKE ? LIMIT 1", (alias,))
            res = self.__cur.fetchone()
            if res:
                return (res['user_name'], res['name'], res['surname'], res['email'], res['phone'],
                        res['profession'], res['about'], json.loads(res['social']))
        except sqlite3.Error as e:
            print(f"Ошибка при получении поста из БД. {e}")
        return False, False, False, False, False, False, False, False

    def updateUserAvatar(self, img, user_id):
        if not img:
            return False
        try:
            binary = sqlite3.Binary(img)
            self.__cur.execute(f"UPDATE profiles SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()

        except sqlite3.Error as e:
            print(f"Ошибка обновления аватара. {e}")
            return False
        return True
