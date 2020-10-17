from db import db
from flask import flash
import accounts, authors, librarymaterial, materialtypes

class Loans(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    material_id = db.Column(db.Integer, nullable=False)
    returned = db.Column(db.Boolean, nullable=False)

    def __init__(self, account_id, material_id, returned):
        self.account_id = account_id
        self.material_id = material_id
        self.returned = False


def loan(account_id, material_id):
    fault = False
    if accounts.user_id() == 0:
        flash("Ei oikeuksia lainaamiseen.")
        fault = True
    if account_id == None or material_id == None:
        flash("Jotain meni pieleen lainauksen kanssa...")
        fault = True
    a_age = accounts.get_account(account_id)[4]
    m_age = librarymaterial.get_work(material_id)[6]
    if m_age > a_age:
        flash("Olet liian nuori tämän sisällön lainaamiseen.")
        fault = True
    loaned = find_loan_count(account_id, material_id)
    if loaned != 0:
        flash("Samaa sisältöä voi olla lainassa samalla henkilöllä kerrallaan vain yksi kappale.")
        fault = True
    if number_of_free(material_id) == 0:
        flash("Kaikki kappaleet ovat lainassa.")
        fault = True
    if fault:
        return False
    sql = "INSERT INTO loans (account_id, material_id, returned) VALUES (:account_id, " \
        ":material_id, False)"
    db.session.execute(sql, {"account_id":account_id, "material_id":material_id})
    db.session.commit()
    return True
    
def find_loan_count(account_id, material_id):
    sql = "SELECT COUNT (*) FROM loans WHERE (account_id=:account_id AND " \
        "material_id=:material_id AND returned=False)"
    result = db.session.execute(sql, {"account_id":account_id, "material_id":material_id})
    loan_count = result.fetchone()[0]
    return loan_count

def find_loan_id(account_id, material_id):
    sql = "SELECT id FROM loans WHERE (account_id=:account_id AND material_id=:material_id " \
        "AND returned=False)"
    result = db.session.execute(sql, {"account_id":account_id, "material_id":material_id})
    loan_id = result.fetchone()[0]
    return loan_id

def get_count():
    result = db.session.execute("SELECT COUNT (*) FROM loans")
    counter = result.fetchone()[0]
    return counter

def number_of_free(material_id):
    sql = "SELECT COUNT (*) FROM loans WHERE material_id=:material_id " \
        "AND returned=False"
    result = db.session.execute(sql, {"material_id":material_id})
    number_of_loaned = result.fetchone()[0]
    number_of_material = librarymaterial.get_work(material_id)[4]
    free = number_of_material - number_of_loaned
    return free

"""def number_of_loans(material_id):
    sql = "SELECT COUNT (*) FROM loans WHERE material_id=:material_id"
    result = db.session.execute(sql, {"material_id":material_id})
    number_of_loans = result.fetchone()[0]
    return number_of_loans"""

def get_loans(account_id):
    sql = "SELECT lo.material_id, li.name, li.type_id, m.name FROM loans lo JOIN " \
        "librarymaterial li ON lo.material_id=li.id JOIN materialtypes m ON " \
        "li.type_id=m.id WHERE lo.account_id=:account_id AND lo.returned=False"
    result = db.session.execute(sql, {"account_id":account_id})
    l_list = result.fetchall()
    return l_list

def get_loan_history():
    #"REPLACE(REPLACE(returned, False, 'Lainassa'), True, 'Palautettu') AS returned "\
    sql = "SELECT li.name, auth.surname, auth.first_name, m.name, acc.name, lo.returned " \
        "FROM loans lo JOIN librarymaterial li ON lo.material_id=li.id JOIN materialtypes " \
        "m ON li.type_id=m.id JOIN authors auth ON li.author_id=auth.id JOIN accounts acc " \
        "ON lo.account_id=acc.id ORDER BY lo.id"
    result = db.session.execute(sql)
    loan_history = result.fetchall()
    return loan_history

def return_loan(account_id, material_id):
    if accounts.user_id() != int(account_id):
        flash("Ei oikeuksia lainan palauttamiseen.")
        return False
    try:
        id = find_loan_id(account_id, material_id)
        loan = Loans.query.get(id)
        loan.returned = True
        db.session.commit() 
        return True
    except:
        return False

def times_loaned(material_id):
    sql = "SELECT COUNT(*) FROM loans WHERE material_id=:material_id"
    result = db.session.execute(sql, {"material_id":material_id})
    times_loaned = result.fetchone()
    return times_loaned