from db import db
from flask import session
import authors, librarymaterial, materialtypes
from werkzeug.security import check_password_hash, generate_password_hash

class Accounts(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)

    def __init__(self, name, username, password, age):
        self.name = name
        self.username = username
        self.password = password
        self.age = age

def login(username, password):
    sql = "SELECT id, password, name FROM accounts WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            session["username"] = user[2]
            session["user_id"] = user[0]
            return True
        else:
            return False

def logout():
    del session["username"]
    del session["user_id"]

def register(name, username, password, age):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO accounts (name, username, password, age) VALUES " \
            "(:name, :username, :password, :age)"
        db.session.execute(sql, {"name":name, "username":username, "password":hash_value, "age":age})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_account(id):
    sql = "SELECT id, name, username, password, age FROM accounts WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    account = result.fetchone()
    return account

def update(id, new_name, new_username, new_age):
    try:
        account = Accounts.query.get(id)
        account.name = new_name
        account.username = new_username
        account.age = new_age
        db.session.commit() 
    except:
        return False

def delete(id):
    try:
        account = Accounts.query.get(id)
        db.session.delete(account)
        db.session.commit()
    except:
        return False

def user_id():
    return session.get("user_id", 0)

