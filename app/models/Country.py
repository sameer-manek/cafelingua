from app.Blueprints import db

class Country(db.Model):

    __tablename__ = "country"
    id = db.Column("id", db.Integer, primary_key = True)
    code = db.Column("country_code", db.String(5))
    name = db.Column("country_name", db.String(50))

    def __init__(self, code, name):
        self.code = code
        self.name = name
