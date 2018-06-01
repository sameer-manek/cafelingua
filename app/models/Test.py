from app.Blueprints import db
from app.models.Grades import Grades

map = db.Table('test_module', db.Column('module_id', db.Integer, db.ForeignKey('module.id')), db.Column('test_id', db.Integer, db.ForeignKey('test.id')))

class Test(db.Model):
    __tablename__ = "test"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)
    date = db.Column("date", db.Date)
    type = db.Column("type", db.Unicode)
    module = db.Column("module_id", db.Integer, db.ForeignKey("module.id"))
    graded = db.Column("graded", db.Integer)
    grades = db.relationship("Grades", backref = db.backref("test"), primaryjoin = id == Grades.test_id)

    link = db.relationship('Course', secondary = map, backref = db.backref('tests'), lazy = 'dynamic')

    def __init__(self, name, date, type, graded = 0):
        self.name = name
        self.type = type
        self.date = date
        self.type = type
        self.graded = graded
