from app import app
from flask import abort, flash, redirect, render_template, request, session
import accounts, authors, librarymaterial, loans, materialtypes
import datetime

@app.route("/")
def index():
    lm_counter = librarymaterial.get_count()
    auth_counter = authors.get_count()
    lo_counter = loans.get_count()
    counters = [lm_counter, auth_counter, lo_counter]
    top5 = loans.most_loaned()
    t_list = materialtypes.get_types_count()
    return render_template("index.html", counters=counters, top5=top5, t_list=t_list)

@app.route("/material_list_by_name")
def material_list_by_name():
    m_list = librarymaterial.get_material_by_name()
    return render_template("material_list.html", m_list=m_list)

@app.route("/material_list_by_type")
def material_list_by_type():
    m_list = librarymaterial.get_material_by_type()
    return render_template("material_list.html", m_list=m_list)
    
@app.route("/material_list_by_author")
def material_list_by_author():
    m_list = librarymaterial.get_material_by_author()
    return render_template("material_list.html", m_list=m_list)

@app.route("/material_list_by_issued")
def material_list_by_issued():
    m_list = librarymaterial.get_material_by_issued()
    return render_template("material_list.html", m_list=m_list)

@app.route("/authors_list")
def authors_list():
    a_list = authors.get_authors()
    return render_template("authors_list.html", a_list=a_list)    

@app.route("/new_author")
def new_author():
    if not accounts.is_admin():
        flash("Ei oikeutta tietojen päivittämiseen.", "warning")
        return redirect("/")
    return render_template("new_author.html")

@app.route("/add_new_author", methods=["POST"])
def add_new_author():
    if not accounts.is_admin():
        flash("Ei oikeutta sisällöntuottajien lisäämiseen.", "warning")
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    fault = False
    first_name = request.form["first_name"].strip()
    if len(first_name) > 40:
        flash("Liian pitkä etunimi.", "warning")
        fault = True
    surname = request.form["surname"].strip()
    if len(surname) == 0:
        flash("Liian lyhyt sukunimi.", "warning")
        fault = True
    if len(surname) > 40:
        flash("Liian pitkä sukunimi.", "warning")
        fault = True
    description = request.form["description"].strip()
    if len(description) > 5000:
        flash("Liian pitkä kuvaus.", "warning")
        fault = True
    if fault:
        flash("Tietojen lisääminen ei onnistunut", "danger")
        return redirect("/")
    if authors.add_new_author(first_name, surname, description, csrf_token):
        flash("Sisällöntuottajan lisääminen järjestelmään onnistui.", "success")
        return redirect("/")
    else:
        flash("Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.", "danger")
        return redirect("/add_new_author") 
    
@app.route("/author/<int:id>")
def author(id):
    author = authors.get_author(id)
    works = librarymaterial.get_works_by_author(id)
    type = materialtypes.get_types()
    return render_template("author.html", id=id, author=author, works=works, type=type)

@app.route("/edit_author", methods=["POST"])
def edit_author():
    csrf_token = request.form["csrf_token"]
    fault = False
    id = request.form["id"]
    new_surname = request.form["new_surname"].strip()
    if len (new_surname) == 0:
        flash("Liian lyhyt sukunimi.", "warning")
        fault = True
    if len(new_surname) > 40:
        flash("Liian pitkä sukunimi.", "warning")
        fault = True
    new_first_name = request.form["new_first_name"].strip()
    if len(new_first_name) > 40:
        flash("Liian pitkä etunimi.", "warning")
        fault = True
    new_description = request.form["new_description"].strip()
    if len(new_description) > 5000:
        flash("Liian pitkä kuvaus.", "warning")
        fault = True
    if fault:
        flash("Tietojen päivittäminen ei onnistunut.", "danger")
        return redirect("/")
    if authors.edit_author(id, new_surname, new_first_name, new_description, csrf_token):
        flash("Sisällöntuottajan tietojen päivitys onnistui.", "success")
        return redirect("/")
    else:
        flash("Tietojen päivittäminen ei onnistunut. Tarkista antamasi tiedot.", "danger")
        return redirect("/")

@app.route("/delete_author", methods=["POST"])
def delete_author():
    csrf_token = request.form["csrf_token"]
    id = request.form["id"]
    if authors.delete_author(id, csrf_token):
        flash("Sisällöntuottaja on poistettu järjestelmästä.", "success")
        return redirect("/")
    else:
        flash("Sisällöntuottajan poistaminen ei onnistunut.", "danger")
        return redirect("/")

@app.route("/add_new_material", methods=["POST"])
def add_new_material():
    if not accounts.is_admin():
        flash("Ei oikeutta tietojen päivittämiseen.", "warning")
        return redirect("/")
    fault = False
    name = request.form["name"].strip()
    if len(name) == 0:
        flash("Sisällöllä täytyy olla nimi.", "warning")
        fault = True
    if len(name) > 140:
        flash("Nimi on liian pitkä.", "warning")
        fault = True
    author_id = request.form["author_id"]
    issued = request.form["issued"]
    if issued == "":
        flash("Anna julkaisuvuosi.", "warning")
        issued = 1000
        fault = True
    if int(issued) < 1700:
        flash("Tarkista julkaisuvuosi.", "warning")
        fault = True
    if int(issued) > datetime.datetime.now().year:
        flash("Tarkista julkaisuvuosi. Kirjastoon otetaan vain jo julkaistua sisältöä.", "warning")
        fault = True
    amount = request.form["amount"]
    if amount == "":
        amount = 0
        flash("Anna kelvollinen lukumäärä.", "warning")
    if int(amount) <= 0:
        flash("Uutta sisältöä on oltava vähintään 1 kappale.", "warning")
        fault = True
    if int(amount) > 100:
        flash("Tämä on nyt jo liikaa...", "warning")
        fault = True 
    type_id = request.form["type_id"]
    age = request.form["age"]
    if age == "":
        flash("Anna kelvollinen ikä.", "warning")
        age = 0
        fault = True
    if int(age) < 0:
        flash("Ikäraja ei voi olla negatiivinen.", "warning")
        fault = True
    if int(age) > 18:
        flash("Kaiken kirjaston materiaalin tulee olla sallittua täysi-ikäisille.", "warning")
        fault = True
    if fault:
        flash("Tietojen lisääminen ei onnistunut.", "danger")
        return redirect("/")
    if librarymaterial.add_new_material(name, author_id, issued, amount, type_id, age):
        flash("Tiedot on lisätty järjestelmään.", "success")
        return redirect("/")
    else:
        flash("Tietojen lisääminen ei onnistunut. Varmista, että olet antanut kaikki tiedot oikein.", "danger")
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
    username = request.form["username"].strip()
    if len(username) > 40:
        flash("Liian pitkä käyttäjätunnus.", "warning")
        return redirect("/")
    password = request.form["password"]
    if len(password) > 16:
        flash("Liian pitkä salasana.", "warning")
        return redirect("/")
    if accounts.login(username, password):
        flash("Olet nyt kirjautunut sisään.", "success")
        return redirect("/")
    else:
        flash("Kirjautuminen ei onnistunut.", "danger")
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
        fault = False
        name = request.form["name"].strip()
        if len(name) == 0:
            flash("Anna jokin nimi.", "warning")
            fault = True
        if len(name) > 100:
            flash("Liian pitkä nimi.", "warning")
            fault = True
        username = request.form["username"].strip()
        if len(username) == 0:
            flash("Anna jokin käyttäjätunnus.", "warning")
        if len(username) > 40:
            flash("Liian pitkä käyttäjätunnus.", "warning")
            fault = True
        password = request.form["password1"]
        password2 = request.form["password2"]
        if password != password2:
            flash("Anna sama salasana kahdesti.", "warning")
            fault = True
        age = request.form["age"]
        if age == "":
            flash("Ikä on pakollinen tieto.", "warning")
            age = 0
            fault = True
        if not 0 < int(age) < 130:
            flash("Anna kelvollinen ikä.", "warning")
            fault = True
        if fault:
            flash("Rekisteröityminen ei onnistunut.", "danger")
            return redirect("/")
        if accounts.register(name, username, password, password2, age):
            flash("Rekisteröityminen onnistui.", "success")
            return redirect("/")
        else:
            flash("Rekisteröityminen ei onnistunut.", "danger")
            return render_template("register.html", name=name, username=username, age=age)

@app.route("/account/<int:id>")
def account(id):
    if not accounts.is_admin():
        id = accounts.user_id()
    account = accounts.get_account(id)
    l_list = loans.get_loans(id)
    l_history = loans.get_personal_loan_history(id)
    return render_template("account.html", account=account, l_list=l_list, l_history=l_history)

@app.route("/update_account", methods=["POST"])
def update_account():
    csrf_token = request.form["csrf_token"]
    fault = False
    id = request.form["id"]
    new_name = request.form["name"].strip()
    if len(new_name) == 0:
        flash("Anna jokin nimi.", "warning")
        fault = True
    if len(new_name) > 100:
        flash("Liian pitkä nimi.", "warning")
        fault = True
    new_username = request.form["username"].strip()
    if len(new_username) == 0:
        flash("Liian lyhyt käyttäjätunnus", "warning")
        fault = True
    if len(new_username) > 40:
        flash("Liian pitkä käyttäjätunnus.", "warning")
        fault = True
    new_age = request.form["age"]
    if new_age == "":
        flash("Ikä on pakollinen tieto.", "warning")
        new_age = 0
        fault = True
    if not 0 <= int(new_age) < 130:
        flash("Anna kelvollinen ikä.", "warning")
        fault = True
    if fault:
        flash("Tietojen päivittäminen ei onnistunut.", "danger")
        return redirect("/")
    if accounts.update(id, new_name, new_username, new_age, csrf_token):
        flash("Tietojen päivittäminen onnistui.", "success")
        return redirect("/")
    else:
        flash("Tietojen päivittäminen ei onnistunut.", "danger")
        return redirect("/")
    
@app.route("/change_password", methods=["POST"])
def change_password():
    csrf_token = request.form["csrf_token"]
    id = request.form["id"]
    old_password = request.form["old_password"]
    password = request.form["new_password"]
    password2 = request.form["new_password2"]
    own_page = "/account/" + id
    if password != password2:
        flash("Salasanat eivät täsmää.", "warning")
        return redirect(own_page)
    if accounts.change_password(id, old_password, password, password2, csrf_token):
        flash("Salasanan vaihtaminen onnistui.", "success")
        return redirect(own_page)
    else:
        flash("Salasanan vaihtaminen ei onnistunut.", "danger")
        return redirect(own_page)

@app.route("/reset_password", methods=["POST"])
def reset_password():
    csrf_token = request.form["csrf_token"]
    if not accounts.is_admin():
        flash("Ei oikeutta salasanan nollaamiseen.", "warning")
        return redirect("/")
    id = request.form["id"]
    username = request.form["username"]
    if accounts.reset_password(id, username, csrf_token):
        flash("Salasanan nollaus onnistui.", "success")
        return redirect("/statistics")
    else:
        flash("Salasanan nollaus ei onnistunut.", "danger")
        return redirect("/statistics")

@app.route("/delete_account", methods=["POST"])
def delete_account():
    id = request.form["id"]
    if accounts.delete_account(id):
        flash("Käyttäjätilin poistaminen onnistui.", "success")
        return redirect("/")
    else:
        flash("Käyttäjätilin poistaminen ei onnistunut.", "danger")
        return redirect("/")

@app.route("/update_material", methods=["POST"])
def update_material():
    if not accounts.is_admin():
        flash("Ei oikeutta tietojen päivittämiseen.", "warning")
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    id = request.form["id"]
    fault = False
    new_name = request.form["new_name"].strip()
    if len(new_name) == 0:
        flash("Nimi on liian lyhyt.", "warning")
        fault = True
    if len(new_name) > 140:
        flash("Nimi on liian pitkä.", "warning")
        fault = True
    new_author_id = request.form["new_author_id"]
    new_issued = request.form["new_issued"]
    if new_issued == "":
        new_issued = 1000
        flash("Anna kelvollinen julkaisuvuosi.", "warning")
    if int(new_issued) < 1700:
        flash("Tarkista julkaisuvuosi. Tällainen sisältö kuuluu museoon.", "warning")
        fault = True
    if int(new_issued) > datetime.datetime.now().year:
        flash("Tarkista julkaisuvuosi. Kirjastoon otetaan vain jo julkaistua sisältöä.", "warning")
        fault = True
    new_amount = request.form["new_amount"]
    if new_amount == "":
        new_amount = 0
        flash("Anna kelvollinen lukumäärä.", "warning")
        fault = True
    if int(new_amount) <= 0:
        flash("Sisältöä on oltava vähintään 1 kappale.", "warning")
        fault = True
    if int(new_amount) > 100:
        flash("Tämä on nyt jo liikaa...", "warning")
        fault = True  
    new_type_id = request.form["new_type_id"]
    new_age = request.form["new_age"]
    if new_age == "":
        new_age = 0
        flash("Anna kelvollinen ikä.", "warning")
        fault = True
    if int(new_age) < 0:
        flash("Ikäraja ei voi olla negatiivinen.", "warning")
        fault = True
    if int(new_age) > 18:
        flash("Kaiken kirjaston materiaalin tulee olla sallittua täysi-ikäisille.", "warning")
        fault = True
    if fault:
        flash("Tietojen lisääminen ei onnistunut.", "danger")
        return redirect("/")
    if librarymaterial.update_material(id, new_name, new_author_id, new_issued, new_amount, new_type_id, new_age, csrf_token):
        flash("Tietojen päivittäminen onnistui.", "success")
        return redirect("/")
    else:
        flash("Tietojen päivittäminen ei onnistunut.", "danger")
        return redirect("/")
    
@app.route("/delete_material", methods=["POST"])
def delete_material():
    id = request.form["id"]
    if librarymaterial.delete_material(id):
        flash("Sisällön poistaminen onnistui.", "success")
        return redirect("/")
    else:
        flash("Sisällön poistaminen ei onnistunut.", "danger")
        return redirect("/")

@app.route("/new_loan", methods=["POST"])
def new_loan():
    account_id = request.form["account_id"]
    material_id = request.form["material_id"]
    if loans.loan(account_id, material_id):
        flash("Lainaaminen onnistui.", "success")
        return redirect("/")
    else:
        flash("Lainaaminen ei onnistunut.", "danger")
        return redirect("/")

@app.route("/return_loan", methods=["POST"])
def return_loan():
    account_id = request.form["account_id"]
    material_id = request.form["material_id"]
    own_page = "/account/" + account_id
    if loans.return_loan(account_id, material_id):
        flash("Palauttaminen onnistui.", "success")
        return redirect(own_page)
    else:
        flash("Palauttaminen ei onnistunut.", "danger")
        return redirect(own_page)

@app.route("/statistics")
def statistics():
    if not accounts.is_admin():
        flash("Ei oikeuksia ylläpitosivulle.", "warning")
        return redirect("/")
    auth_list = authors.get_authors()
    m_list = librarymaterial.get_material_by_name()
    type_list = materialtypes.get_types()
    acc_list = accounts.get_accounts()
    loan_history = loans.get_loan_history()
    return render_template("statistics.html", auth_list=auth_list, m_list=m_list, type_list=type_list, acc_list=acc_list, loan_history=loan_history)

@app.route("/edit_type")
def edit_type():
    if not accounts.is_admin():
        flash("Ei oikeuksia tyyppien muuttamiseen.", "warning")
        return redirect("/")
    id = request.form["id"]
    new_name = request.form["new_name"].strip()
    if not 0 < len(new_name) < 20:
        flash("Tyypillä kuuluu olla korkeintaan 20 merkkiä pitkä nimi.", "warning")
    if materialtypes.edit_type(id, new_name):
        flash("Tyypin muuttaminen onnistui.", "success")
        return redirect("/statistics")
    else:
        flash("Tyypin muuttaminen ei onnistunut.", "danger")
        return redirect("/statistics")

@app.route("/delete_type", methods=["POST"])
def delete_type():
    id = request.form["id"]
    if materialtypes.delete_type(id):
        flash("Tyypin poistaminen onnistui.", "success")
        return redirect("/")
    else:
        flash("Tyypin poistaminen ei onnistunut.", "danger")
        return redirect("/")