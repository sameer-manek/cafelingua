from app.Blueprints import db, connection
from time import strftime
from app.models.Batch import Batch
from app.models.Test import Test
from app.models.Grades import Grades

map = db.Table('batch_student', db.Column('batch_id', db.Integer, db.ForeignKey('batch.id')), db.Column('student_id', db.Integer, db.ForeignKey('student_master.id')))

class Student(db.Model):
    __tablename__ = "student_master"
    id = db.Column("id", db.Integer, primary_key = True)
    RFID = db.Column("RFID", db.Integer)
    fname = db.Column("first_name", db.Unicode)
    lname = db.Column("last_name", db.Unicode)
    email = db.Column("email", db.Unicode, unique = True)
    passwd = db.Column("passwd", db.Unicode)
    mobile = db.Column("mobile", db.Unicode, unique = True)
    DOB = db.Column("DOB", db.Date)
    picture = db.Column("picture", db.Unicode)
    reg_date = db.Column("reg_date", db.Date)
    source = db.Column("source", db.Unicode)
    comp_date = db.Column("comp_date", db.Date)
    state = db.Column("state", db.Integer)
    link = db.relationship('Batch', secondary=map, backref=db.backref('students'), lazy='dynamic')
    grades = db.relationship("Grades", backref=db.backref("students"), primaryjoin=id == Grades.student_id)

    def __init__(self, fname, lname, email, RFID, mobile, DOB, source):
        passwd = fname+" "+lname
        picture = "default.jpg"
        state = 1
        reg_date = strftime("%Y-%m-%d")
        self.fname = fname
        self.lname = lname
        self.email = email
        self.passwd = passwd
        self.RFID = RFID
        self.mobile = mobile
        self.reg_date = reg_date
        self.picture = picture
        self.DOB = DOB
        self.source = source
        self.state = state