from app.Blueprints import db

class Grades(db.Model):

    __tablename__ = "test_student"
    test_id = db.Column("test_id", db.Integer, db.ForeignKey("test.id"), primary_key=True)
    student_id = db.Column("student_id", db.Integer, db.ForeignKey("student_master.id"), primary_key=True)
    grade = db.Column("grade", db.Float, nullable=True)