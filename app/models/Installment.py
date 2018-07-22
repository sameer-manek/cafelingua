from app.Blueprints import db

class Installment(db.Model):
    __tablename__ = "installment"
    id = db.Column("id", db.Integer, primary_key = True)
    student = db.Column("student_id", db.Integer, db.ForeignKey("student_master.id"))
    date = db.Column("date", db.Date)
    amount = db.Float("amount", db.Float, default=0)

    def __init__(self, student, date, amount):
        self.student = student
        self.date = date
        self.amount = amount
