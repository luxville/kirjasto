from db import db
from flask import abort, session
import accounts

class Materialtypes(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
        

def get_types_count():
    sql = "SELECT M.id, M.name, COUNT(L.type_id) FROM materialtypes M JOIN " \
        "Librarymaterial L ON M.id=L.type_id WHERE L.type_id=M.id GROUP BY " \
        "M.id ORDER BY M.name"
    result = db.session.execute(sql)
    t_list = result.fetchall()
    return t_list

def get_type(id):
    sql = "SELECT M.id, M.name FROM materialtypes M JOIN librarymaterial L ON " \
        "L.type_id=M.id WHERE L.id=:id"
    result = db.session.execute(sql, {"id":id})
    type = result.fetchone()
    return type

def get_types():
    sql = "SELECT id, name FROM materialtypes"
    result = db.session.execute(sql)
    t_list = result.fetchall()
    return t_list

def edit_type(id, new_name):
    if not accounts.is_admin():
        return False
    try:
        type = Materialtypes.query.get(id)
        type.name = new_name
        db.session.commit() 
        return True
    except:
        return False

def delete_type(id):
    if not accounts.is_admin():
        return False
    try:
        type = Materialtypes.query.get(id)
        db.session.delete(type)
        db.session.commit()
        return True
    except:
        return False