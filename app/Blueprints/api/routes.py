from flask import Blueprint, Response, jsonify, request, render_template, session, escape
from time import strftime
import json

mod_api = Blueprint('api', __name__)

@mod_api.route("/punch", methods=["GET"])
def punch():
    from app.models.key import Key
    from app.models.Attendance import Attendance

    RFID = request.args.get("rfid")
    DATE = strftime("%Y-%m-%d")
    TIME = strftime("%H:%M:%S")
    KEY = request.args.get("key")
    res = 0
    if RFID == None or RFID == '':
        return jsonify(res)
    if Key.query.filter_by(key = KEY).first() is not None:
        from app.models.Student import Student
        if Student.query.filter_by(RFID = RFID).first() is not None:
            res = Attendance.punch(key=KEY, rfid=RFID, date = DATE, time = TIME)
    return jsonify(res)

@mod_api.route("/batch/students/<batchid>", methods=["POST"])
def fetchStudentsFromBatch(batchid):
    if session.get("user") == True and session['type'] == "admin":
        key = request.form.get("key")
        from app.models.key import Key

        chk = Key.query.filter_by(key = key).first()
        if chk is not None:
            from app.models.Batch import Batch
            from app.models.Student import Student

            batch = Batch.query.get(batchid)
            students = []
            for student in batch.students:
                arr = {
                    "id" : student.id,
                    "name" : student.fname+" "+student.lname
                }
                students.append(arr)
            return jsonify(students)

@mod_api.route("/student/scores/<studentId>", methods=["GET"])
def fetchGrades(studentId):
    if session.get("user") == True and session['type'] == "admin":
        from app.Blueprints import db
        from app.models.Grades import Grades
        from app.models.Test import Test
        all_tests = db.session.query(Grades).filter(Grades.student_id == studentId).all()
        csv = "test,grade,module,date" + escape("\n")
        for i in all_tests:
            test = db.session.query(Test).filter(Test.id == i.test_id).first()
            print(test.module)
            csv = csv + str(test.name) + "," + str(i.grade) + "," + str(test.module) + "," + str(test.date) + escape("\n")
            print(i.grade)
        return str(csv)

    else:
        return "Error"
