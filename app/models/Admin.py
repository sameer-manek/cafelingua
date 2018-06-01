from app.Blueprints import db
from flask import session

class Admin(db.Model):
    __tablename__ = "admin_master"
    id = db.Column("id", db.Integer, primary_key = True)
    email = db.Column("email", db.Unicode)
    passwd = db.Column("passwd", db.Unicode)
    first_name = db.Column("first_name", db.Unicode)
    last_name = db.Column("last_name", db.Unicode)

    def __init__(self, fname, lname, email, passwd):
        self.email = email
        self.passwd = passwd
        self.first_name = fname
        self.last_name = lname

