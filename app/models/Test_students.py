from app.models.Test import Test
from app.models.Student import Student
from app.Blueprints import db

class Test_Students(db.Model):
    __tablename__ = "test_student"
    test = db.Column("test_id", db.Integer, db.ForeignKey('test.id'))
    student = db.Column("student_id", db.Integer, db.ForeignKey("student.id"))
    grade = db.Column("grade", db.Float, nullable = True)

    tests = db.relationship(Test, backref="students")
    students = db.relationship(Student, backref="tests")
