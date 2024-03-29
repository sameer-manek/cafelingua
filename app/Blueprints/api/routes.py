from flask import Blueprint, Response, jsonify, request, render_template, session, escape, current_app as application
from time import strftime
import json

mod_api = Blueprint('api', __name__)

@mod_api.route("/punch", methods=["GET"])
def punch():
    from app.models.key import Key
    from app.models.Attendance import Attendance
    from app.Blueprints import write_key
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
    write_key(RFID)
    
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

@mod_api.route("/batch/<batch_id>/modules", methods = ["GET"])
def get_batch_routes(batch_id):
    from app.models.Batch import Batch
    from app.models.Course import Course
    from app.models.Module import Module
    from app.Blueprints import db
    batch = Batch.query.get(batch_id)
    i = list()
    for course in batch.courses:
        for module in course.modules:
            init = {
                "module_id" : module.id,
                "module_name" : module.name,
                "module_mm" : module.maxMarks
            }
            i.append(init)
    return jsonify(i)


@mod_api.route("/batch/<batch_id>/student_avg", methods=['GET'])
def student_avg(batch_id):
    if session.get("user") == True and session['type'] == "admin" : 
        from app.Blueprints import db
        from app.models.Course import Course
        from app.models.Module import Module
        from app.models.Batch import Batch
        from app.models.Test import Test
        from app.models.Student import Student
        from app.models.Grades import Grades

        csv = "batch,student,module,grade,max" + escape('\n')
        batch = Batch.query.get(batch_id)

        for student in batch.students:
            grades = Grades.query.filter_by(student_id = student.id)
            for grade in grades:
                test = Test.query.get(grade.test_id)
                module = Module.query.get(test.module_id)
                csv = csv + batch.name + ',' + student.fname+' '+student.lname + ',' + module.name + ',' + float(grade.grade) + ',' + float(module.max)
    return str(csv)

@mod_api.route("/module/<batch_id>/scores", methods=['GET'])
def mod_score(batch_id):
    if session.get("user") == True and session['type'] == "admin":
        from app.Blueprints import db
        from app.models.Course import Course
        from app.models.Module import Module
        from app.models.Batch import Batch
        from app.models.Test import Test
        from app.models.Student import Student
        from app.models.Grades import Grades
        batch = Batch.query.get(batch_id)
        csv = "module,avg,max" + escape("\n")
        maxMarks = 0
        for course in batch.courses:
            for module in course.modules:
                maxMarks = module.maxMarks
                grades = list()
                if (module.tests):
                    for test in module.tests:
                        # find average grade
                        for i in test.grades:
                            grades.append(float(i.grade))
                    i = sum(grades)/len(grades)
                    csv = csv + str(module.name) + "," + str(float(i)) + "," + str(float(module.maxMarks)) + escape("\n")
        
    return str(csv)
