from app.Blueprints import db

class Admin(db.Model):
    __tablename__ = "admin_master"
    id = db.Column("id", db.Integer, primary_key = True)
    email = db.Column("email", db.String(75))
    passwd = db.Column("passwd", db.String(75))
    first_name = db.Column("first_name", db.String(25))
    last_name = db.Column("last_name", db.String(25))

    def __init__(self, fname, lname, email, passwd):
        self.email = email
        self.passwd = passwd
        self.first_name = fname
        self.last_name = lname
