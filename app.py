from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes


"""
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
#from .models import Accounts



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

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

@app.route("/")
def index():
    sql = "SELECT m.id, m.name, t.name FROM material m JOIN types t ON m.type_id=t.id " \
        "WHERE m.type_id=t.id ORDER BY m.name"
    result = db.session.execute(sql)
    material = result.fetchall()
    result = db.session.execute("SELECT COUNT (*) FROM authors")
    count_a = result.fetchone()[0]
    sql = "SELECT id, surname, first_name FROM authors ORDER BY surname"
    result = db.session.execute(sql)
    authors = result.fetchall()
    sql = "SELECT t.id, t.name, COUNT(m.type_id) FROM types t JOIN material m ON " \
        "t.id=m.type_id WHERE m.type_id=t.id GROUP BY t.id ORDER BY t.name"
    result = db.session.execute(sql)
    types = result.fetchall()
    return render_template("index.html", material=material, count_a=count_a, authors=authors, types=types)

#@app.route("/result", methods=["POST"])
#def result():
#    return render_template("result.html",name=request.form["name"]) 
    #request.form kun pyydetään tietoja lomakkeelta

@app.route("/new_author")
def new_author():
    return render_template("new_author.html")

@app.route("/add_new_author", methods=["POST"])
def add_new_author():
    first_name = request.form["first_name"]
    surname = request.form["surname"]
    born = request.form["born"]
    dead = request.form["dead"]
    description = request.form["description"]
    sql = "INSERT INTO authors (first_name, surname, born, dead, description) VALUES " \
        "(:first_name, :surname, :born, :dead, :description)"
    db.session.execute(sql, {"first_name":first_name,"surname":surname,"born":born,"dead":dead,"description":description})
    db.session.commit()
    return redirect("/")

@app.route("/author/<int:id>")
def author(id):
    sql = "SELECT id, surname, first_name, born, dead, description FROM authors " \
        "WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    author = result.fetchone()
    sql = "SELECT id, name, author_id FROM material WHERE author_id=:id"
    result = db.session.execute(sql, {"id":id})
    works = result.fetchall()
    sql = "SELECT id, name FROM types ORDER BY name"
    result = db.session.execute(sql)
    types = result.fetchall()
    return render_template("author.html", id=id, author=author, works=works, types=types)

@app.route("/add_new_material", methods=["POST"])
def add_new_material():
    name = request.form["name"]
    author_id = request.form["author_id"]
    issued = request.form["issued"]
    amount = request.form["amount"]
    type_id = request.form["type_id"]
    age = request.form["age"]
    sql = "INSERT INTO material (name, author_id, issued, amount, type_id, age) " \
        "VALUES (:name, :author_id, :issued, :amount, :type_id, :age)"
    db.session.execute(sql, {"name":name, "author_id":author_id, "issued":issued, "amount":amount, "type_id":type_id, "age":age})
    db.session.commit()
    return redirect("/")

@app.route("/material/<int:id>")
def material(id):
    sql = "SELECT id, name, author_id, issued, amount, type_id, age FROM material " \
        "WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    work = result.fetchone()
    sql = "SELECT a.id, a.surname, a.first_name FROM authors a JOIN material m ON " \
        "m.author_id=a.id WHERE m.id=:id"
    result = db.session.execute(sql, {"id":id})
    author = result.fetchone()
    sql = "SELECT t.name FROM types t JOIN material m ON m.type_id=t.id WHERE m.id=:id"
    result = db.session.execute(sql, {"id":id})
    type = result.fetchone()
    return render_template("material.html", id=id, work=work, author=author, type=type)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password, name FROM accounts WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        redirect("/")
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            session["username"] = user[2]
            session["user_id"] = user[0]
            redirect("/")
        else:
            redirect("/")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password1"]
    hash_value = generate_password_hash(password)
    age = request.form["age"]
    sql = "INSERT INTO accounts (name, username, password, age) VALUES " \
        "(:name, :username, :password, :age)"
    db.session.execute(sql, {"name":name, "username":username, "password":hash_value, "age":age})
    db.session.commit()
    return redirect("/")

@app.route("/account/<int:id>")
def account(id):
    sql = "SELECT id, name, username, password, age FROM accounts WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    account = result.fetchone()
    return render_template("account.html", account=account)

@app.route("/update_account", methods=["POST"])
def update_account():
    id = request.form["id"]
    new_name = request.form["name"]
    new_username = request.form["username"]
    new_age = request.form["age"]
    account = Accounts.query.get(id)
    account.name = new_name
    account.username = new_username
    account.age = new_age
    db.session.commit() 
    return redirect("/")

@app.route("/delete_account", methods=["POST"])
def delete():
    id = request.form["id"]
    account = Accounts.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return redirect("/")

    """