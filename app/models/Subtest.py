from Blueprints import db

class Subtest(db.Model):
    __tablename__ = "subtest"
    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(40))
    test_id = db.Column("test_id", db.Integer, db.ForeignKey('test.id'))

    def __init__(self, name, test_id):
        self.name = name
        self.test_id = test_id
