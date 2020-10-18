from db import db
from flask import abort, flash, request, session
# import authors, librarymaterial, loans, materialtypes
from werkzeug.security import check_password_hash, generate_password_hash
import os

class Accounts(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)
    #access = db.Column(db.String(5), nullable=False)

    def __init__(self, name, username, password, age): #, access):
        self.name = name
        self.username = username
        self.password = password
        self.age = age
        #self.access = access


def is_admin():
    sql = "SELECT access FROM accounts WHERE id=:user"
    result = db.session.execute(sql, {"user":user_id()})
    access = result.fetchone()[0]
    if access == "admin":
        return True
    return False

def login(username, password):
    sql = "SELECT id, password, name, access FROM accounts WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        flash("Käyttäjätunnusta ei löydy. Tarkista käyttäjätunnus tai rekisteröidy.", "warning")
        return False
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            session["username"] = user[2]
            session["user_id"] = user[0]
            session["csrf_token"] = os.urandom(16).hex()
            session["access"] = user[3]
            return True
        else:
            flash("Salasana ja käyttäjätunnus eivät täsmää. Tarkista tiedot.", "warning")
            return False

def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    del session["access"]

def register(name, username, password, password2, age):
    if password != password2:
        return False
    if not 0 < int(age) < 130:
        return False
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO accounts (name, username, password, age) VALUES " \
            "(:name, :username, :password, :age)"
        db.session.execute(sql, {"name":name, "username":username, "password":hash_value, "age":age})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_account(id):
    if not is_admin():
        id = user_id()
    sql = "SELECT id, name, username, password, age FROM accounts WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    account = result.fetchone()
    return account

def get_accounts():
    if user_id() == 0:
        return []
    sql = "SELECT id, name, username, age FROM accounts WHERE access='user'"
    result = db.session.execute(sql, {"id":id})
    acc_list = result.fetchall()
    return acc_list

def update(id, new_name, new_username, new_age, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    id = user_id()
    if not 0 <= int(new_age) < 130:
        return False
    try:
        account = Accounts.query.get(id)
        account.name = new_name
        account.username = new_username
        account.age = new_age
        db.session.commit() 
        return True
    except:
        flash("Jokin meni pieleen.", "danger")
        return False

def change_password(id, old_password, password, password2, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    user = user_id()
    if user != int(id):
        return False
    if password != password2:
        return False
    else:
        sql = "SELECT password FROM accounts WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        user = result.fetchone()
        if not check_password_hash(user[0], old_password):
            flash("Tarkista vanha salasana.", "warning")
            return False
        else:
            try:
                account = Accounts.query.get(id)
                account.password = generate_password_hash(password)
                db.session.commit() 
                return True
            except:
                return False

def reset_password(id, username, csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
    if not is_admin():
        return False
    try:
        account = Accounts.query.get(id)
        account.password = generate_password_hash(username)
        db.session.commit()
        flash("Salasana on nyt sama kuin käyttäjätunnus.", "success")
        return True
    except:
        return False

def delete_account(id):
    if user_id() != int(id) and not is_admin():
        return False
    try:
        account = Accounts.query.get(id)
        db.session.delete(account)
        db.session.commit()
        logout()
        return True
    except:
        return False

def user_id():
    return session.get("user_id", 0)