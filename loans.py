from db import db
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
    if account_id == None or material_id == None:
        return False
    a_age = accounts.get_account(account_id)[4]
    m_age = librarymaterial.get_work(material_id)[6]
    if m_age > a_age:
        return False
    loaned = find_loan_count(account_id, material_id)
    if loaned != 0:
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

def number_of_free(material_id):
    sql = "SELECT COUNT (material_id) FROM loans WHERE material_id=:material_id"
    result = db.session.execute(sql, {"material_id":material_id})
    number_of_loans = result.fetchone()[0]
    number_of_material = librarymaterial.get_work(material_id)[4]
    free = number_of_material - number_of_loans
    return free

def get_loans(account_id):
    sql = "SELECT lo.material_id, li.name, li.type_id, m.name FROM loans lo JOIN " \
        "librarymaterial li ON lo.material_id=li.id JOIN materialtypes m ON " \
        "li.type_id=m.id WHERE lo.account_id=:account_id AND lo.returned=False"
    result = db.session.execute(sql, {"account_id":account_id})
    l_list = result.fetchall()
    return l_list

def return_loan(account_id, material_id):
    id = find_loan_id(account_id, material_id)
    try:
        loan = Loans.query.get(id)
        loan.returned = True
        db.session.commit() 
        return True
    except:
        return False