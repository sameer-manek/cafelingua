from app.Blueprints import db
from app.models.Course import Course

map = db.Table('course_module', db.Column('module_id', db.Integer, db.ForeignKey('module.id')), db.Column('course_id', db.Integer, db.ForeignKey('course.id')))

class Module(db.Model):
    __tablename__ = "module"
    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.Unicode)
    desc = db.Column("desc", db.Unicode)
    duration = db.Column("duration", db.Integer)
    maxMarks = db.Column("maximum_marks", db.Float)

    link = db.relationship('Course', secondary = map, backref = db.backref('modules'), lazy = 'dynamic')

    def __init__(self, name, desc, duration):
        self.name = name
        self.desc = desc
        self.duration = duration
