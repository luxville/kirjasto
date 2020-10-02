from db import db
import accounts, material, types

class Authors(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    born = db.Column(db.Integer)
    dead = db.Column(db.Integer)
    description = db.Column(db.String(1000))

    def __init__(self, first_name, surname, born, dead, description):
        self.first_name = first_name
        self.surname = surname
        self.born = born
        self.dead = dead
        self.description = description

def add_new_author(first_name, surname, born, dead, description):
    if first_name == None or surname == None or born == None or dead == None or description == None:
        return False
    sql = "INSERT INTO authors (first_name, surname, born, dead, description) VALUES " \
        "(:first_name, :surname, :born, :dead, :description)"
    db.session.execute(sql, {"first_name":first_name,"surname":surname,"born":born,"dead":dead,"description":description})
    db.session.commit()
    return True

def get_author(id):
    sql = "SELECT id, surname, first_name, born, dead, description FROM authors " \
        "WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    author = result.fetchone()
    return author

def get_author_by_work(id):
    sql = "SELECT A.id, A.surname, A.first_name FROM authors A JOIN librarymaterial L " \
        "ON L.author_id=A.id WHERE L.id=:id"
    result = db.session.execute(sql, {"id":id})
    author = result.fetchone()
    return author

def get_authors():
    sql = "SELECT id, surname, first_name FROM authors ORDER BY surname"
    result = db.session.execute(sql)
    a_list = result.fetchall()
    return a_list

def get_count():
    result = db.session.execute("SELECT COUNT (*) FROM authors")
    counter = result.fetchone()[0]
    return counter

