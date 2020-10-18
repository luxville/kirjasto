from db import db
from flask import abort, request, session
import accounts

class Authors(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(1000))

    def __init__(self, first_name, surname, description):
        self.first_name = first_name
        self.surname = surname
        self.description = description


def add_new_author(first_name, surname, description, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    if not accounts.is_admin():
        return False
    if first_name == None or surname == None or description == None:
        return False
    sql = "INSERT INTO authors (first_name, surname, description) VALUES " \
        "(:first_name, :surname, :description)"
    db.session.execute(sql, {"first_name":first_name,"surname":surname,"description":description})
    db.session.commit()
    return True

def edit_author(id, new_surname, new_first_name, new_description, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    if not accounts.is_admin():
        return False
    try:
        author = Authors.query.get(id)
        author.surname = new_surname
        author.first_name = new_first_name
        author.description = new_description
        db.session.commit() 
        return True
    except:
        return False

def delete_author(id, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    if not accounts.is_admin():
        return False
    try:
        author = Authors.query.get(id)
        db.session.delete(author)
        db.session.commit()
        return True
    except:
        return False

def get_author(id):
    sql = "SELECT id, surname, first_name, description FROM authors WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    author = result.fetchone()
    return author

def get_author_by_work(id):
    sql = "SELECT a.id, a.surname, a.first_name FROM authors a JOIN librarymaterial l " \
        "ON l.author_id=a.id WHERE l.id=:id"
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

