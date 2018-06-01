from app.Blueprints import db
from app.models.Batch import Batch

map = db.Table('batch_course', db.Column('course_id', db.Integer, db.ForeignKey('course.id')), db.Column('batch_id', db.Integer, db.ForeignKey('batch.id')))

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.Unicode)
    link = db.relationship('Batch', secondary=map, backref=db.backref('courses'), lazy='dynamic')

    def __init__(self, name):
        self.name = name
