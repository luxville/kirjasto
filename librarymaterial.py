from db import db
from flask import abort, session
import accounts, authors, loans, materialtypes

class Librarymaterial(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    issued = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, author_id, issued, amount, type_id, age):
        self.name = name
        self.author_id = author_id
        self.issued = issued
        self.amount = amount
        self.type_id = type_id
        self.age = age


def add_new_material(name, author_id, issued, amount, type_id, age):
    if not accounts.is_admin():
        return False
    faults = False
    if name == None or author_id == None or amount == None or type_id == None:
        faults = True
    if age != None:
        if int(age) < 0:
            faults = True
        if int(age) > 18:
            faults = True
    if int(amount) < 0:
        faults = True
    if faults:
        return False
    sql = "INSERT INTO librarymaterial (name, author_id, issued, amount, type_id, age) " \
        "VALUES (:name, :author_id, :issued, :amount, :type_id, :age)"
    db.session.execute(sql, {"name":name, "author_id":author_id, "issued":issued, "amount":amount, "type_id":type_id, "age":age})
    db.session.commit()
    return True

def get_count():
    result = db.session.execute("SELECT COUNT (*) FROM librarymaterial")
    counter = result.fetchone()[0]
    return counter

def count_works(id):
    result = db.session.execute("SELECT COUNT (id), IFNULL(COUNT(id), 0), FROM " \
        "librarymaterial WHERE author_id=id")
    counter = result.fetchone()[0]
    return counter

def get_material_by_name():
    sql = "SELECT l.id, l.name, m.name, m.id, a.surname, a.first_name, l.issued FROM " \
        "librarymaterial l JOIN materialtypes m ON l.type_id=m.id JOIN authors a ON " \
        "l.author_id=a.id WHERE l.type_id=m.id ORDER BY l.name"
    result = db.session.execute(sql)
    m_list = result.fetchall()
    return m_list

def get_material_by_author():
    sql = "SELECT l.id, l.name, m.name, m.id, a.surname, a.first_name, l.issued FROM " \
        "librarymaterial l JOIN materialtypes m ON l.type_id=m.id JOIN authors a ON " \
        "l.author_id=a.id WHERE l.type_id=m.id ORDER BY a.surname, a.first_name"
    result = db.session.execute(sql)
    m_list = result.fetchall()
    return m_list

def get_material_by_type():
    sql = "SELECT l.id, l.name, m.name, m.id, a.surname, a.first_name, l.issued FROM " \
        "librarymaterial l JOIN materialtypes m ON l.type_id=m.id JOIN authors a ON " \
        "l.author_id=a.id WHERE l.type_id=m.id ORDER BY l.name"
    result = db.session.execute(sql)
    m_list = result.fetchall()
    return m_list

def get_material_by_issued():
    sql = "SELECT l.id, l.name, m.name, m.id, a.surname, a.first_name, l.issued FROM " \
        "librarymaterial l JOIN materialtypes m ON l.type_id=m.id JOIN authors a ON " \
        "l.author_id=a.id WHERE l.type_id=m.id ORDER BY l.issued DESC"
    result = db.session.execute(sql)
    m_list = result.fetchall()
    return m_list

def get_work(id):
    sql = "SELECT id, name, author_id, issued, amount, type_id, age FROM librarymaterial " \
        "WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    work = result.fetchone()
    return work

def get_works_by_author(id):
    sql = "SELECT id, name, author_id FROM librarymaterial WHERE author_id=:id"
    result = db.session.execute(sql, {"id":id})
    works = result.fetchall()
    return works

def update_material(id, new_name, new_author_id, new_issued, new_amount, new_type_id, new_age, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    if not accounts.is_admin():
        return False
    if new_age != None:
        if int(new_age) < 0:
            return False
        if int(new_age) > 18:
            return False
    if int(new_amount) < 0:
        return False
    try:
        material = Librarymaterial.query.get(id)
        material.name = new_name
        material.author_id = new_author_id
        material.issued = new_issued
        material.amount = new_amount
        material.type_id = new_type_id
        material.age = new_age
        db.session.commit() 
        return True
    except:
        return False

def delete_material(id):
    if not accounts.is_admin():
        return False
    try:
        material = Librarymaterial.query.get(id)
        db.session.delete(material)
        db.session.commit()
        return True
    except:
        return False