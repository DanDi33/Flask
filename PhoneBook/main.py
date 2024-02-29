from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
import os.path

app = Flask(__name__)
app.config["SECRET_KEY"] = "wewrtrtey1223345dfgdf"

menu = [
    {"title": "Main", "url": '/'},
    {"title": "Добавить номер", "url": '/addnum'},
    {"title": "Добавить организацию", "url": '/addcompany'}
]


def connect_db():
    connection = sqlite3.connect('my_database.db')
    return connection


def create_db():
    db = connect_db()
    cur = db.cursor()
    with app.open_resource("sql_db.sql", mode="r") as f:
        cur.executescript(f.read())
        # скрипт для тестов
        cur.executescript('''
        insert INTO Professions (profession) values('Директор'),('Исполнительный директор'),('Диспетчер');
        insert INTO FIO (lastName,firstName,patronymic) values ('Данилов','Дмитрий','Олегович'),
        ('Белякова','Оксана','Анатольевна');
        insert INTO Types(type) values ('Сотовый'),('Рабочий'),('Домашний');
        insert INTO Companies (companyName) values ('УК Люкс'),('Оникс'),('БэстСтрой'),('ГУК'),('КЭЧ'),
        ('ТСН «Высотка»'),('ТСЖ "Кондоминиум №1'),('ТСЖ "Большие Ременники"'),('Горизонт'),('АДС');
        insert INTO Workers (companyId,fioId,professionId) values (10,1,1),(10,2,3),(9,2,2);
        insert INTO Phones (typeId,number) values (2,'544935'),(2,'366958'),(1,'9005551111'),(1,'9206262222');
        insert INTO WorkPhones (workerId,phoneId) values (1,2),(1,4),(2,2),(2,3),(3,3),(3,1);
        ''')
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


def get_data_from_db(tablename):
    db = get_db()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {tablename}")
    res = cur.fetchall()
    return res


def show_numbers():
    db = get_db()
    cur = db.cursor()
    cur.execute('''select C.companyName,Pr.profession,(F.lastName||" "||F.firstName||" "||F.patronymic),T.type,P.number 
from Phones as P 
join Types as T on P.typeId= T.id 
join WorkPhones as WP on WP.phoneId = P.id 
join Workers as W on WP.workerId = W.id
join FIO as F on W.fioId = F.id
join Companies as C on W.companyId=C.id
join Professions as Pr on W.professionId = Pr.id
order by companyName, lastName
;''')
    res = cur.fetchall()
    return res


@app.route("/")
def index():
    title = "Список контактов"

    data = show_numbers()
    res = {}
    fio = {}
    professions = {}

    for i, el in enumerate(data):
        phones = fio.get(el[2], {})
        phones.update({el[4]: el[3]})
        # print(f"fio[el[2]] = {fio.get(el[2], {})}")
        fio = professions.get(el[1], {})
        fio.update({el[2]: phones})
        # print(f"professions[el[1]] = {professions.get(el[1], {})}")
        professions = res.get(el[0], {})
        professions.update({el[1]: fio})
        res.update({el[0]: professions})
        # print(f"res[el[0]] = {res.get(el[0], {})}")
        # print(f"i = {i},el = {el}")

    # print(res)
    return render_template("index.html", menu=menu, title=title, data=data, res=res)


@app.route("/addnum", methods=["POST", "GET"])
def add_num():
    title = "Добавление контакта"

    if not os.path.exists("my_database.db"):
        create_db()
    comp_form = get_data_from_db("Companies")
    prof_form = get_data_from_db("Professions")
    type_form = get_data_from_db("Types")
    if request.method == "POST":
        if ((len(request.form['surname']) > 2 and
             len(request.form['name']) > 2 and
             len(request.form['patronymic']) > 4 and
             len(request.form['company']) > 2) and
                len(request.form['number']) > 5):
            res = (request.form['company'], request.form['profession'], request.form['type'], request.form['number'],
                   request.form['surname'], request.form['name'], request.form['patronymic'])
            print(res)
            if not res:
                flash("Ошибка добавления", category="error")
            else:
                flash("Успешно добавлено", category="success")
        else:
            flash("Ошибка добавления, проверьте ваши данные", category="error")
            return redirect(url_for("add_num"))
        try:
            db = get_db()
            cur = db.cursor()

            # НУЖНО ДОПИСАТЬ СКРИПТ ДОБАВЛЕНИЯ КОНТАКТА
            cur.execute("INSERT INTO Companies VALUES (NULL,?)", (res,))
            db.commit()

        except:
            print("Error adding cotact")
        finally:
            return redirect(url_for("add_num"))
    return render_template("addnum.html", menu=menu, title=title, comp_form=comp_form, prof_form=prof_form,
                           type_form=type_form)


@app.route("/addcompany", methods=["POST", "GET"])
def add_company():
    title = "Добавление организации"

    if not os.path.exists("my_database.db"):
        create_db()
    if request.method == "POST":
        if len(request.form['name']) > 4:
            res = request.form['name']
            print(res)
            if not res:
                flash("Ошибка добавления", category="error")
            else:
                flash("Успешно добавлено", category="success")
        else:
            flash("Ошибка добавления, проверьте ваши данные", category="error")
            return redirect(url_for("add_company"))
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO Companies VALUES (NULL,?)", (res,))
            db.commit()
            return redirect(url_for("add_company"))
        except:
            print("Error adding post")
    return render_template("addcompany.html", menu=menu, title=title)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
