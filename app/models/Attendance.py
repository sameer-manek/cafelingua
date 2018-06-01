from app.Blueprints import db, connection

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column('id', db.Integer, primary_key = True)
    RFID = db.Column('RFID', db.Unicode)
    date = db.Column('date', db.Date)
    in_time = db.Column('in_time', db.Time)
    out_time = db.Column('out_time', db.Time)

    def punch(key, rfid, date, time):
        qry = "SELECT * FROM api_key WHERE unique_key = '" + key + "'"
        proxy = connection.execute(qry)
        results = proxy.fetchall()
        if len(results) > 0:
            qry = "SELECT * FROM attendance WHERE RFID = '"+rfid+"' AND d_date = '"+date+"' AND out_time IS NULL"
            proxy = connection.execute(qry)
            results = proxy.fetchall()
            if len(results) > 0:
                qry = "UPDATE attendance SET out_time = '"+time+"' WHERE RFID = '"+rfid+"' AND d_date = '"+date+"' AND out_time IS NULL"
                connection.execute(qry)
            else:
                qry = "INSERT INTO attendance(RFID, d_date, in_time) VALUES('"+rfid+"', '"+date+"', '"+time+"')"
                connection.execute(qry)
            res = 1
            return res
        else:
            res = 0
            return res