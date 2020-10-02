from db import db
from flask import session
import accounts, authors, material

def get_types_count():
    sql = "SELECT M.id, M.name, COUNT(L.type_id) FROM materialtypes M JOIN " \
        "Librarymaterial L ON M.id=L.type_id WHERE L.type_id=M.id GROUP BY " \
        "M.id ORDER BY M.name"
    result = db.session.execute(sql)
    t_list = result.fetchall()
    return t_list

def get_type_name(id):
    sql = "SELECT M.name FROM materialtypes M JOIN librarymaterial L ON " \
        "L.type_id=M.id WHERE L.id=:id"
    result = db.session.execute(sql, {"id":id})
    type = result.fetchone()
    return type

def get_types():
    sql = "SELECT id, name FROM materialtypes"
    result = db.session.execute(sql)
    t_list = result.fetchall()
    return t_list

#def get_types_by_author(id):
#    sql = "SELECT id, name, author_id FROM material WHERE author_id=:id"
#    result = db.session.execute(sql, {"id":id})
#    works = result.fetchall()
#    return works