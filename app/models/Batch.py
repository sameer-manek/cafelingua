from app.Blueprints import db
from time import strftime

class Batch(db.Model):
    __tablename__ = "batch"
    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("batch_name", db.String(90))
    start_date = db.Column("start_date", db.Date)
    comp_date = db.Column("comp_date", db.Date)
    day_byte = db.Column("day_byte", db.String(7))
    start_time = db.Column("start_time", db.Time)
    duration = db.Column("duration", db.Integer)

    def __init__(self, name, daybyte, start_time, duration):
        date = strftime("%Y-%m-%d")
        self.name = name
        self.day_byte = daybyte
        self.start_date = date
        self.start_time = start_time
        self.duration = duration
