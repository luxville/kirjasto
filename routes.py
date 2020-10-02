from app import app
from flask import redirect, render_template, request, session
import accounts, authors, librarymaterial, materialtypes

@app.route("/")
def index():
    m_list = librarymaterial.get_material()
    counter = authors.get_count()
    a_list = authors.get_authors()
    t_list = materialtypes.get_types_count()
    return render_template("index.html", m_list=m_list, counter=counter, a_list=a_list, t_list=t_list)

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
    if authors.add_new_author(first_name, surname, born, dead, description):
        return redirect("/")
    else:
        return render_template("error.html", message="Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.")
    
@app.route("/author/<int:id>")
def author(id):
    author = authors.get_author(id)
    works = librarymaterial.get_works_by_author(id)
    type = materialtypes.get_types()
    return render_template("author.html", id=id, author=author, works=works, type=type)

@app.route("/add_new_material", methods=["POST"])
def add_new_material():
    name = request.form["name"]
    author_id = request.form["author_id"]
    issued = request.form["issued"]
    amount = request.form["amount"]
    type_id = request.form["type_id"]
    age = request.form["age"]
    if librarymaterial.add_new_material(name, author_id, issued, amount, type_id, age):
        return redirect("/")
    else:
        return render_template("error.html", message="Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.")

@app.route("/material/<int:id>")
def material(id):
    work = librarymaterial.get_work(id)
    author = authors.get_author_by_work(id)
    type = materialtypes.get_type_name(id)
    return render_template("material.html", id=id, work=work, author=author, type=type)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if accounts.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Kirjautuminen ei onnistunut. Käyttäjätunnus ja salasana eivät täsmää.")

@app.route("/logout")
def logout():
    accounts.logout()
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password1"]
        age = request.form["age"]
        if accounts.register(name, username, password, age):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröityminen ei onnistunut.")

@app.route("/account/<int:id>")
def account(id):
    account = accounts.get_account(id)
    return render_template("account.html", account=account)

@app.route("/update_account", methods=["POST"])
def update_account():
    id = request.form["id"]
    new_name = request.form["name"]
    new_username = request.form["username"]
    new_age = request.form["age"]
    if accounts.update(id, new_name, new_username, new_age):
        return redirect("/")
    else:
        return render_template("error.html", message="Tietojen päivittäminen ei onnistunut.")
    
@app.route("/delete_account", methods=["POST"])
def delete():
    id = request.form["id"]
    if accounts.delete(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Käyttäjätilin poistaminen ei onnistunut.")
    