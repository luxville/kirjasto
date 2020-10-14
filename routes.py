from app import app
from flask import redirect, render_template, request, session
import accounts, authors, librarymaterial, loans, materialtypes

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
    description = request.form["description"]
    if authors.add_new_author(first_name, surname, description):
        return redirect("/")
    else:
        return render_template("error.html", message="Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.")
    
@app.route("/author/<int:id>")
def author(id):
    author = authors.get_author(id)
    works = librarymaterial.get_works_by_author(id)
    type = materialtypes.get_types()
    return render_template("author.html", id=id, author=author, works=works, type=type)

@app.route("/edit_author", methods=["POST"])
def edit_author():
    id = request.form["id"]
    new_surname = request.form["new_surname"]
    new_first_name = request.form["new_first_name"]
    new_description = request.form["new_description"]
    if authors.edit_author(id, new_surname, new_first_name, new_description):
        return redirect("/")
    else:
        return render_template("error.html", message="Tietojen päivittäminen ei onnistunut.")

@app.route("/delete_author", methods=["POST"])
def delete_author():
    id = request.form["id"]
    if authors.delete_author(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Sisällöntuottajan poistaminen ei onnistunut.")

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
    free = loans.number_of_free(id)
    a_list = authors.get_authors()
    type = materialtypes.get_type(id)
    t_list = materialtypes.get_types()
    return render_template("material.html", id=id, work=work, author=author, free=free, a_list=a_list, type=type, t_list=t_list)

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
    l_list = loans.get_loans(id)
    return render_template("account.html", account=account, l_list=l_list)

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
def delete_account():
    id = request.form["id"]
    if accounts.delete_account(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Käyttäjätilin poistaminen ei onnistunut.")

@app.route("/update_material", methods=["POST"])
def update_material():
    id = request.form["id"]
    new_name = request.form["new_name"]
    new_author_id = request.form["new_author_id"]
    new_issued = request.form["new_issued"]
    new_amount = request.form["new_amount"]
    new_type_id = request.form["new_type_id"]
    new_age = request.form["new_age"]
    if librarymaterial.update_material(id, new_name, new_author_id, new_issued, new_amount, new_type_id, new_age):
        return redirect("/")
    else:
        return render_template("error.html", message="Tietojen päivittäminen ei onnistunut.")
    
@app.route("/delete_material", methods=["POST"])
def delete_material():
    id = request.form["id"]
    if librarymaterial.delete_material(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Teoksen poistaminen ei onnistunut.")

@app.route("/new_loan", methods=["POST"])
def new_loan():
    account_id = request.form["account_id"]
    material_id = request.form["material_id"]
    if loans.loan(account_id, material_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Lainaaminen ei onnistunut.")

@app.route("/return_loan", methods=["POST"])
def return_loan():
    account_id = request.form["account_id"]
    material_id = request.form["material_id"]
    if loans.return_loan(account_id, material_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Palauttaminen ei onnistunut.")