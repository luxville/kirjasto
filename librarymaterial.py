from db import db
import accounts, authors, types

class Librarymaterial(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    issued = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    type = db.Column(db.Integer)
    age = db.Column(db.Integer)

    def __init__(self, name, author_id, issued, amount, type, age):
        self.name = name
        self.author_id = author_id
        self.issued = issued
        self.amount = amount
        self.type = type
        self.age = age

def add_new_material(name, author_id, issued, amount, type_id, age):
    if name == None or author_id == None or issued == None or amount == None or type_id == None or age == None:
        return False
    sql = "INSERT INTO librarymaterial (name, author_id, issued, amount, type_id, age) " \
        "VALUES (:name, :author_id, :issued, :amount, :type_id, :age)"
    db.session.execute(sql, {"name":name, "author_id":author_id, "issued":issued, "amount":amount, "type_id":type_id, "age":age})
    db.session.commit()
    return True

def get_material():
    sql = "SELECT L.id, L.name, M.name FROM librarymaterial L, materialtypes M WHERE " \
        "L.type_id=M.id ORDER BY L.name"
    result = db.session.execute(sql)
    m_list = result.fetchall()
    return m_list

def get_work(id):
    sql = "SELECT id, name, author_id, issued, amount, type_id, age FROM " \
        "librarymaterial WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    work = result.fetchone()
    return work

def get_works_by_author(id):
    sql = "SELECT id, name, author_id FROM librarymaterial WHERE author_id=:id"
    result = db.session.execute(sql, {"id":id})
    works = result.fetchall()
    return works