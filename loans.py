from db import db
# import accounts, authors, librarymaterial, materialtypes

class Loans(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    material_id = db.Column(db.Integer, nullable=False)

    def __init__(self, account_id, material_id):
        self.account_id = account_id
        self.material_id = material_id


def loan(account_id, material_id):
    if account_id == None or material_id == None:
        return False
    #sql = "SELECT a.age, l.age CAST (CASE WHEN l.age > a.age THEN 1 ELSE 0 END AS BIT) " \
    #    "FROM accounts a, librarymaterial l WHERE a.id=account_id AND l.id=material_id"
    #underage = db.session.execute(sql, {"account_id":account_id, "material_id":material_id})
    #if underage:
    #    return False
    sql = "INSERT INTO loans (account_id, material_id) VALUES (:account_id, :material_id)"
    db.session.execute(sql, {"account_id":account_id, "material_id":material_id})
    db.session.commit()
    return True