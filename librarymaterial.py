from db import db
import accounts, authors, materialtypes

class Librarymaterial(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    issued = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

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

def update_material(id, name, author_id, issued, amount, type, age):
    sql = "UPDATE librarymaterial SET name=:name, author_id=:author_id, " \
        "issued=:issued, amount=:amount, type=:type, age=:age WHERE id=:id"
    result = db.session.execute(sql,{"name":name, "author_id":author_id, "issued":issued, "amount":amount, "type":type, "age":age, "id":id})
    db.session.commit()
    """
    try:
        material = Librarymaterial.query.get(id)
        material.name = new_name
        material.author_id = new_author_id
        material.issued = new_issued
        material.amount = new_amount
        material.type = new_type
        material.age = new_age
        db.session.commit() 
        return True
    except:
        return False
"""

def delete_material(id):
    try:
        material = Librarymaterial.query.get(id)
        db.session.delete(material)
        db.session.commit()
        return True
    except:
        return False