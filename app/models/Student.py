from app.Blueprints import db
from time import strftime
from app.models.Batch import Batch
from app.models.Test import Test
from app.models.Grades import Grades

map = db.Table('batch_student', db.Column('batch_id', db.Integer, db.ForeignKey('batch.id')), db.Column('student_id', db.Integer, db.ForeignKey('student_master.id')))

class Student(db.Model):
    __tablename__ = "student_master"
    id = db.Column("id", db.Integer, primary_key = True)
    RFID = db.Column("RFID", db.Integer)
    fname = db.Column("first_name", db.String(25))
    lname = db.Column("last_name", db.String(25))
    email = db.Column("email", db.String(100), unique = True)
    passwd = db.Column("passwd", db.String(70))
    mobile = db.Column("mobile", db.String(20), unique = True)
    DOB = db.Column("DOB", db.Date)
    picture = db.Column("picture", db.String(100))
    reg_date = db.Column("reg_date", db.Date)
    source = db.Column("source", db.String(50))
    grade10 = db.Column("grade10", db.Float, nullable = True)
    grade12 = db.Column("grade12", db.Float, nullable = True)
    graduate = db.Column("graduation", db.Float, nullable = True)
    PG = db.Column("post_graduate", db.Float, nullable = True)
    NOB = db.Column("NOB", db.Integer, nullable = True)
    country = db.Column("country_id", db.Integer, db.ForeignKey("country.id"))
    comp_date = db.Column("comp_date", db.Date)
    state = db.Column("state", db.Integer)
    link = db.relationship('Batch', secondary=map, backref=db.backref('studs'), lazy='dynamic')
    grades = db.relationship("Grades", backref=db.backref("students"), primaryjoin=id == Grades.student_id)

    def __init__(self, fname, lname, email, RFID, mobile, DOB, source, grade10, grade12, graduate, PG, NOB, country):
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
        self.grade10 = grade10
        self.grade12 = grade12
        self.graduate = graduate
        self.PG = PG
        self.NOB = NOB
        self.country = country
