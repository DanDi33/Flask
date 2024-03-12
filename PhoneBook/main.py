from flask import Flask, render_template, request, redirect, url_for, g, flash, session
import sqlite3
import os.path

app = Flask(__name__)
app.config["SECRET_KEY"] = "wewrtrtey1223345dfgdf"

menu = [
    {"title": "Main", "url": '/'},
    {"title": "Добавить номер", "url": '/addnum'},
    {"title": "Добавить организацию", "url": '/addcompany'},
    {"title": "Добавить профессию", "url": '/addprof'}
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
        # print(f"i = {i},el = {el}")
        # print(f"el[0]={el[0]}, data[i-1][0]={data[i-1][0]}")
        if el[0] != data[i - 1][0]:
            fio = {}

        phones = fio.get(el[2], {})
        phones.update({el[4]: el[3]})

        fio = professions.get(el[1], {})
        fio.update({el[2]: phones})
        # print(f"fio[el[2]] = {fio.get(el[2], {})}")

        professions = res.get(el[0], {})
        professions.update({el[1]: fio})
        # print(f"professions[el[1]] = {professions.get(el[1], {})}")
        res.update({el[0]: professions})
        # print(f"res[el[0]] = {res.get(el[0], {})}")

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
            try:
                db = get_db()
                cur = db.cursor()
                error = False

                # Проверяю в БД название компании, если нет - добавляю. Возвращаю id
                cur.execute("SELECT id FROM Companies WHERE companyName = ?",
                            (res[0],))
                company_id = cur.fetchone()
                if company_id is None:
                    cur.execute("INSERT INTO Companies (companyName) VALUES(?)",
                                (res[0],))
                    company_id = cur.lastrowid
                    print(f"company_id(added) = {company_id}")
                else:
                    company_id = company_id[0]
                    print(f"company_id(was) = {company_id}")

                # Проверяю в БД название профессии, если нет - добавляю. Возвращаю id
                cur.execute("SELECT id FROM Professions WHERE profession = ?",
                            (res[1],))
                profession_id = cur.fetchone()
                if profession_id is None:
                    cur.execute("INSERT INTO Professions (profession) VALUES(?)",
                                (res[1],))
                    profession_id = cur.lastrowid
                    print(f"profession_id(added) = {profession_id}")
                else:
                    profession_id = profession_id[0]
                    print(f"profession_id(was) = {profession_id}")

                # Проверяю в БД полное совпадение ФИО, если нет - добавляю. Возвращаю id
                cur.execute("SELECT id FROM FIO WHERE lastName=? and firstName=? and patronymic = ?",
                            (res[4], res[5], res[6],))
                fio_id = cur.fetchone()
                if fio_id is None:
                    cur.execute("INSERT INTO FIO (lastName,firstName,patronymic) VALUES(?,?,?)",
                                (res[4], res[5], res[6],))
                    fio_id = cur.lastrowid
                    print(f"fio_id(added) = {fio_id}")
                else:
                    fio_id = fio_id[0]
                    print(f"fio_id(was) = {fio_id}")

                # Проверяю в БД сотрудника, если нет - добавляю. Возвращаю id
                cur.execute("SELECT id FROM Workers WHERE fioId=? and professionId=? and companyId = ?",
                            (fio_id, profession_id, company_id,))
                worker_id = cur.fetchone()
                if worker_id is None:
                    cur.execute("INSERT INTO Workers (fioId, professionId, companyId) VALUES(?,?,?)",
                                (fio_id, profession_id, company_id,))
                    worker_id = cur.lastrowid
                    print(f"worker_id(added) = {worker_id}")
                else:
                    worker_id = worker_id[0]
                    print(f"worker_id(was) = {worker_id}")

                # Проверяю в БД тип номера, если нет - добавляю. Возвращаю id
                cur.execute("SELECT id FROM Types WHERE type=?",
                            (res[2],))
                type_id = cur.fetchone()
                if type_id is None:
                    cur.execute("INSERT INTO Types (type) VALUES(?)",
                                (res[2],))
                    type_id = cur.lastrowid
                    print(f"type_id(added) = {type_id}")
                else:
                    type_id = type_id[0]
                    print(f"type_id(was) = {type_id}")

                # Проверяю в БД номер телефона, если нет - добавляю. Возвращаю id
                cur.execute("SELECT id FROM Phones WHERE number = ?",
                            (res[3],))
                phone_id = cur.fetchone()
                if phone_id is None:
                    cur.execute("INSERT INTO Phones (typeId, number) VALUES(?,?)",
                                (type_id, res[3],))
                    phone_id = cur.lastrowid
                    print(f"phone_id(added) = {phone_id}")
                else:
                    phone_id = phone_id[0]
                    print(f"phone_id(was) = {phone_id}")

                # Проверяю в БД с рабочим номером сотрудника, если нет - добавляю,
                # если есть возвращаю error(Сотрудник существует)
                cur.execute("SELECT id FROM WorkPhones WHERE workerId=? and phoneId=?",
                            (worker_id, phone_id,))
                work_phone_id = cur.fetchone()
                if work_phone_id is None:
                    cur.execute("INSERT INTO WorkPhones (workerId, phoneId) VALUES(?,?)",
                                (worker_id, phone_id,))
                    work_phone_id = cur.lastrowid
                    print(f"work_phone_id(added) = {work_phone_id}")
                else:
                    work_phone_id = work_phone_id[0]
                    print(f"work_phone_id(was) = {work_phone_id}")
                    error = "Сотрудник с таким номером существует."

                db.commit()
                # return redirect(url_for("add_num"))
            except Exception as e:
                error = e
                print("Error adding cotact", e)
            if not res or error is not False:
                flash(f"Ошибка добавления. {error}", category="error")
                return redirect(url_for("add_num"))
            else:
                flash("Успешно добавлено", category="success")
                return redirect(url_for("add_num"))
        else:
            flash("Ошибка добавления, проверьте ваши данные", category="error")
            return redirect(url_for("add_num"))

    return render_template("addnum.html", menu=menu, title=title, comp_form=comp_form, prof_form=prof_form,
                           type_form=type_form)


@app.route("/addcompany", methods=["POST", "GET"])
def add_company():
    title = "Добавление организации"
    error = False
    print(session.pop('_flashes', None))

    if not os.path.exists("my_database.db"):
        create_db()
    if request.method == "POST":
        if len(request.form['name']) > 2:
            res = request.form['name']
            print(res)
            try:
                db = get_db()
                cur = db.cursor()
                cur.execute("SELECT id FROM Companies WHERE companyName=?", (res,))
                company_id = cur.fetchone()
                if company_id is None:
                    cur.execute("INSERT INTO Companies (companyName) VALUES(?)", (res,))
                    company_id = cur.lastrowid
                    print(f"company_id(added) = {company_id}")
                else:
                    company_id = company_id[0]
                    print(f"company_id(was) = {company_id}")
                    error = "Компания с таким названием уже существует."
                db.commit()
            except Exception as e:
                error = e
                print(f"Error adding post. {e}")
            if not res or error is not False:
                flash(f"Ошибка добавления. {error}", category="error")
                # return redirect(url_for("add_company"))
            else:
                flash("Успешно добавлено", category="success")
                return redirect(url_for("add_company"))
        else:
            flash("Ошибка добавления, проверьте ваши данные", category="error")
            # return redirect(url_for("add_company"))

    return render_template("addcompany.html", menu=menu, title=title)


@app.route("/addprof", methods=["POST", "GET"])
def add_profession():
    title = "Добавление профессии"
    error = False

    if not os.path.exists("my_database.db"):
        create_db()
    if request.method == "POST":
        if len(request.form['name']) > 4:
            res = request.form['name']
            print(res)
            try:
                db = get_db()
                cur = db.cursor()
                cur.execute("SELECT id FROM Professions WHERE profession=?", (res,))
                profession_id = cur.fetchone()
                if profession_id is None:
                    cur.execute("INSERT INTO Professions (profession) VALUES(?)", (res,))
                    profession_id = cur.lastrowid
                    print(f"profession_id(added) = {profession_id}")
                else:
                    profession_id = profession_id[0]
                    print(f"profession_id(was) = {profession_id}")
                    error = "Такая профессия уже существует."
                db.commit()
            except Exception as e:
                error = e
                print(f"Error adding profession. {e}")
            if not res or error is not False:
                flash(f"Ошибка добавления. {error}", category="error")
                return redirect(url_for("add_profession"))
            else:
                flash("Успешно добавлено", category="success")
                return redirect(url_for("add_profession"))
        else:
            flash("Ошибка добавления, проверьте ваши данные", category="error")
            return redirect(url_for("add_profession"))
    return render_template("addprof.html", menu=menu, title=title)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


if __name__ == "__main__":
    app.run(host='192.168.1.65', debug=True)
    # app.run(host='192.168.10.165', debug=True)
