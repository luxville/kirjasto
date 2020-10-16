from app import app
from flask import flash, redirect, render_template, request, session
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
    if not accounts.is_admin():
        flash("Ei oikeuksia sisällöntuottajien lisäämiseen.")
        return redirect("/")
    first_name = request.form["first_name"]
    surname = request.form["surname"]
    description = request.form["description"]
    if authors.add_new_author(first_name, surname, description):
        flash("Sisällöntuottajan lisääminen järjestelmään onnistui.")
        return redirect("/")
    else:
        flash("Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.")
        return redirect("/add_new_author") #render_template("error.html", message="x")
    
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
        flash("Sisällöntuottajan tietojen päivitys onnistui.")
        return redirect("/")
    else:
        flash("Tietojen päivittäminen ei onnistunut. Tarkista antamasi tiedot.")
        return redirect("/")

@app.route("/delete_author", methods=["POST"])
def delete_author():
    id = request.form["id"]
    if authors.delete_author(id):
        flash("Sisällöntuottaja on poistettu järjestelmästä.")
        return redirect("/")
    else:
        flash("Sisällöntuottajan poistaminen ei onnistunut.")
        return redirect("/")

@app.route("/add_new_material", methods=["POST"])
def add_new_material():
    name = request.form["name"]
    author_id = request.form["author_id"]
    issued = request.form["issued"]
    amount = request.form["amount"]
    type_id = request.form["type_id"]
    age = request.form["age"]
    if librarymaterial.add_new_material(name, author_id, issued, amount, type_id, age):
        flash("Tiedot on lisätty järjestelmään.")
        return redirect("/")
    else:
        flash("Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.")
        return redirect("/")

@app.route("/material/<int:id>")
def material(id):
    work = librarymaterial.get_work(id)
    author = authors.get_author_by_work(id)
    free = loans.number_of_free(id)
    times_loaned = loans.times_loaned(id)
    a_list = authors.get_authors()
    type = materialtypes.get_type(id)
    t_list = materialtypes.get_types()
    return render_template("material.html", id=id, work=work, author=author, free=free, times_loaned=times_loaned, a_list=a_list, type=type, t_list=t_list)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if accounts.login(username, password):
        return redirect("/")
    else:
        flash("Kirjautuminen ei onnistunut.")
        return redirect("/")

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
        password2 = request.form["password2"]
        age = request.form["age"]
        if accounts.register(name, username, password, password2, age):
            flash("Rekisteröityminen onnistui.")
            return redirect("/")
        else:
            flash("Rekisteröityminen ei onnistunut.")
            return render_template("register.html", name=name, username=username, age=age)

@app.route("/account/<int:id>")
def account(id):
    if not accounts.is_admin():
        id = accounts.user_id()
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
        flash("Tietojen päivittäminen onnistui.")
        return redirect("/")
    else:
        flash("Tietojen päivittäminen ei onnistunut.")
        return redirect("/")
    
@app.route("/change_password", methods=["POST"])
def change_password():
    id = request.form["id"]
    old_password = request.form["old_password"]
    password = request.form["new_password"]
    password2 = request.form["new_password2"]
    own_page = "/account/" + id
    if accounts.change_password(id, old_password, password, password2):
        flash("Salasanan vaihtaminen onnistui.")
        return redirect(own_page)
    else:
        flash("Salasanan vaihtaminen ei onnistunut.")
        return redirect(own_page)

@app.route("/reset_password", methods=["POST"])
def reset_password():
    id = request.form["id"]
    username = request.form["username"]
    if accounts.reset_password(id, username):
        flash("Salasanan nollaus onnistui.")
        return redirect("/maintenance")
    else:
        flash("Salasanan nollaus ei onnistunut.")
        return redirect("/maintenance")

@app.route("/delete_account", methods=["POST"])
def delete_account():
    id = request.form["id"]
    if accounts.delete_account(id):
        flash("Käyttäjätilin poistaminen onnistui.")
        return redirect("/")
    else:
        flash("Käyttäjätilin poistaminen ei onnistunut.")
        return redirect("/")

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
        flash("Tietojen päivittäminen onnistui.")
        return redirect("/")
    else:
        flash("Tietojen päivittäminen ei onnistunut.")
        return redirect("/")
    
@app.route("/delete_material", methods=["POST"])
def delete_material():
    id = request.form["id"]
    if librarymaterial.delete_material(id):
        flash("Teoksen poistaminen onnistui.")
        return redirect("/")
    else:
        flash("Teoksen poistaminen ei onnistunut.")
        return redirect("/")

@app.route("/new_loan", methods=["POST"])
def new_loan():
    account_id = request.form["account_id"]
    material_id = request.form["material_id"]
    if loans.loan(account_id, material_id):
        flash("Lainaaminen onnistui.")
        return redirect("/")
    else:
        flash("Lainaaminen ei onnistunut.")
        return redirect("/")

@app.route("/return_loan", methods=["POST"])
def return_loan():
    account_id = request.form["account_id"]
    material_id = request.form["material_id"]
    own_page = "/account/" + account_id
    if loans.return_loan(account_id, material_id):
        flash("Palauttaminen onnistui.")
        return redirect(own_page)
    else:
        flash("Palauttaminen ei onnistunut.")
        return redirect(own_page)

@app.route("/maintenance")
def maintenance():
    if not accounts.is_admin():
        flash("Ei oikeuksia ylläpitosivulle.")
        return redirect("/")
    auth_list = authors.get_authors()
    m_list = librarymaterial.get_material()
    type_list = materialtypes.get_types()
    acc_list = accounts.get_accounts()
    loan_history = loans.get_loan_history()
    return render_template("maintenance.html", auth_list=auth_list, m_list=m_list, type_list=type_list, acc_list=acc_list, loan_history=loan_history)