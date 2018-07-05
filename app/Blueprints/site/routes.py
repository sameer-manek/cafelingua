from flask import Blueprint, render_template, request, session, redirect, jsonify, current_app as application
import json
mod_site = Blueprint("site", __name__, template_folder="templates")


# site general pages
@mod_site.route("/")
def homepage():
    return render_template("home.html")


@mod_site.route("/services")
def servicePage():
    return render_template("services.html")


@mod_site.route("/stories")
def stories():
    return render_template("stories.html")


@mod_site.route("/about")
def aboutpage():
    return render_template("about.html")


@mod_site.route("/contact")
def contactpage():
    return render_template("contact.html")

@mod_site.route("/logout")
def logout():
    if session.get("user") == True:
        from app.Blueprints import db
        db.session.commit()
        session.clear()
    return redirect("/")


# student pages

@mod_site.route("/login", methods=["GET", "POST"])
def loginpage():
    return "this is student login page" 

@mod_site.route("/student")
def accessStudent():
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Student import Student
        from app.Blueprints import db
        with open(application.config['JSON_FILE'], 'r') as jsonFile:
            data = json.load(jsonFile)
        lastcard = data['lastcard']
        jsonFile.close()

        students = Student.query.filter_by(state=1)
        return render_template("admin/student/browse.html", students=students, username = fetchusername(), lastcard = lastcard)
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/student/new", methods=["GET", "POST"])
def registerStudent():
    if session.get("user") == True and session["type"] == "admin":
        from app.Blueprints import db
        from app.models.Batch import Batch
        from app.models.Student import Student
        from app.models.Country import Country

        batches = Batch.query.all()
        countries = Country.query.all()
        if request.method == "POST":
            for value in request.form:
                if request.form[value] == '':
                    return render_template("admin/student/student_registration.html", msg="all fields are necessary")

            cnts = request.form.getlist("country[]")
            cstr = ''
            for cnt in cnts:
                cstr += ' {},'.format(cnt)

            newStudent = Student(fname = request.form.get("fname"), lname = request.form.get("lname"), email = request.form.get("email"),
                                 RFID = request.form.get("RFID"), mobile = request.form.get("phone"), DOB = request.form.get("DOB"),
                                 source = request.form.get("source"), grade10 = request.form.get('grade10'), grade12 = request.form.get('grade12'), graduate = request.form.get('graduate'), PG = request.form.get('PG'), NOB = request.form.get('NOB'), country = cstr)

            db.session.add(newStudent)
            db.session.commit()
            batch = Batch.query.get(request.form.get('batch'))
            batch.studs.append(newStudent)
            return render_template("admin/student/student_registration.html",
                                   msg="student has been succefully registered!", username = fetchusername(), batches = batches, countries = countries)

        return render_template("admin/student/student_registration.html", username = fetchusername(), batches = batches, countries = countries)
    else:
        return render_template("errors/not_authorised.html")

@mod_site.route("/student/<id>/about", methods = ["GET"])
def aboutStudent(id):
    if session.get("user") == True and session['type'] == "admin":
        from app.models.Student import Student
        from app.Blueprints import db
        from app.models.Grades import Grades
        from app.models.Test import Test
        from app.models.Module import Module
        all_tests = db.session.query(Grades).filter(Grades.student_id == id).all()
        csv = "test,grade,module,date,name" + "\\n"
        maxMarks = 0
        for i in all_tests:
            test = db.session.query(Test).filter(Test.id == i.test_id).first()
            module = db.session.query(Module).filter(Module.id == test.module).first()
            maxMarks = module.maxMarks
            print("Maxmarks: " + str(maxMarks))
            csv = csv + str(test.name) + "," + str(i.grade) + "," + str(test.module) + "," + str(test.date) + "," + str(module.name) + "\\n"
        student = Student.query.get(id)
        if student == None:
            return "no record exists"
        else:
            return render_template("admin/student/about.html", student = student, username = fetchusername(), csv=csv, maxMarks = maxMarks)

@mod_site.route("/student/<id>/deactivate", methods = ['GET'])
def deactivate_student(id):
    if session.get('user') and session.get('type') == "admin":
        # valid access
        from app.Blueprints import db
        from app.models.Student import Student

        student = Student.query.get(id)
        if student is not None:
            try:
                student.state = 0
                db.session.commit()
            except Exception as e:
                return "there was some problem on the backend"
            return redirect("/student")
        else:
            return "could not deactivate student"
    else:
        return render_template("errors/not_authorised.html")


# admin pages
@mod_site.route("/admin", methods=["GET", "POST"])
def accessAdmin():
    if session.get("user") == True and session["type"] == "admin":
        return redirect("admin/dashboard")
    else:
        return redirect("admin/login")


@mod_site.route("/admin/login", methods=["GET", "POST"])
def adminLogin():
    if (request.method == "POST"):
        email = request.form.get('email')
        passwd = request.form.get('passwd')

        from app.models.Admin import Admin
        from app.Blueprints import db

        admin = db.session.query(Admin).filter_by(email = email, passwd = passwd).first()
        if admin is not None:
            session['user'] = admin.id
            session['type'] = 'admin'
            return redirect("/student")
        else:
            return render_template("admin/login.html", message="invalid creds")
    else:
        return render_template("admin/login.html")
 
@mod_site.route("/admin/dashboard")
def loadAdminDashboard():
    if (session.get("user") == True and session['type'] == "admin"):
        from app.models.Admin import Admin
        from app.Blueprints import db

        user = Admin.query.filter_by(id=session["user"]).first()
       
        return render_template("admin/dashboard.html", usr=user, username = fetchusername(), lastcard = lastcard)
    else:
        return redirect("/admin/login")


# Modules
@mod_site.route("/module")
def accessModules():
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Module import Module
        from app.Blueprints import db

        modules = Module.query.all()
        return render_template("admin/module/browse.html", modules=modules, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/module/new", methods=["GET", "POST"])
def addModule():
    if session.get("user") == True and session["type"] == "admin":
        if request.method == "POST":
            for field in request.form:
                if request.form[field] == '':
                    return render_template("admin/module/add_module.html", msg="please fill up all the fields")
            # process data
            from app.models.Module import Module
            from app.Blueprints import db

            newModule = Module(request.form.get("name"), request.form.get("desc"), int(request.form.get("days")), float(request.form.get("maxMarks")))
            db.session.add(newModule)
            db.session.commit()
            return render_template("admin/module/add_module.html", msg="module is successfully added", username = fetchusername())
        return render_template("admin/module/add_module.html", username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/module/update/<module_id>", methods=["GET", "POST"])
def updateModule(module_id):
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Module import Module
        from app.Blueprints import db

        curMod = Module.query.get(module_id)
        if request.method == "POST":
            for field in request.form:
                if request.form[field] == '':
                    return render_template("admin/module/update_module.html",
                                           msg="update failed, reason : you left some fields empty", module=curMod, username = fetchusername())
            curMod.name = request.form.get("name")
            curMod.desc = request.form.get("desc")
            curMod.duration = request.form.get("duration")
            curMod.maxMarks = request.form.get("maxMarks")
            db.session.commit()
            return render_template("admin/module/update_module.html", msg="updated the module", module=curMod, username = fetchusername())

        return render_template("admin/module/update_module.html", module=curMod, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/module/delete/<module_id>")
def deleteModule(module_id):
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Module import Module
        from app.Blueprints import db

        curMod = Module.query.get(module_id)
        db.session.delete(curMod)
        db.session.commit()
        return redirect("/module")
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/course")
def accessCourses():
    if session.get("user") == True and session['type'] == "admin":
        from app.models.Course import Course
        from app.Blueprints import db

        courses = Course.query.all()
        return render_template("admin/course/browse.html", courses=courses, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/course/new", methods=["GET", "POST"])
def addCourse():
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Module import Module
        mods = Module.query.all()
        if request.method == "POST":
            from app.models.Course import Course
            from app.Blueprints import db

            newCourse = Course(request.form.get('name'))
            db.session.add(newCourse)
            db.session.commit()

            moduleList = request.form.getlist("moduleList[]")
            for mod in moduleList:
                module = Module.query.get(mod)
                newCourse.modules.append(module)
            db.session.commit()
            return render_template("admin/course/add_course.html", modules=mods,
                                   msg="course has been successfully added", username = fetchusername())
        return render_template("admin/course/add_course.html", modules=mods, username = fetchusername())

    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/course/delete/<course_id>")
def deleteCourse(course_id):
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Course import Course
        from app.Blueprints import db

        course = Course.query.get(course_id)
        course.modules = []
        db.session.delete(course)
        db.session.commit()
        courses = Course.query.all()
        return redirect("/course")
    else:
        return render_template("errors/not_authorised.html", username = fetchusername())


@mod_site.route("/course/about/<course_id>")
def aboutCourse(course_id):
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Course import Course
        from app.Blueprints import db

        course = Course.query.get(course_id)
        return render_template("admin/course/about_course.html", course=course, modules=course.modules, username = fetchusername())


# Batches

@mod_site.route("/batch")
def accessBatches():
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Batch import Batch
        from app.Blueprints import db

        batches = Batch.query.all()
        return render_template("admin/batch/browse.html", batches=batches, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/batch/new", methods=["GET", "POST"])
def createBatch():
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Batch import Batch
        from app.models.Student import Student
        from app.models.Course import Course
        from app.Blueprints import db

        students = Student.query.all()
        courses = Course.query.all()

        if request.method == "POST":
            for field in request.form:
                if request.form[field] == "":
                    return render_template("admin/batch/create_batch.html", courses=courses, students=students,
                                           msg="please fill up all the fields", username = fetchusername())
            daylist = request.form.getlist("dayList[]")
            arr = [0, 0, 0, 0, 0, 0, 0]
            for ele in daylist:
                arr[int(ele)] = 1
            daybyte = r = int("".join(map(str, arr)))
            newsBatch = Batch(request.form.get("name"), daybyte, request.form.get("time"), request.form.get("duration"))
            db.session.add(newsBatch)
            db.session.commit()
            for student in request.form.getlist("studentList[]"):
                stud = Student.query.get(student)
                newsBatch.students.append(stud)
            cr = Course.query.get(request.form.get("course"))
            newsBatch.courses.append(cr)
            db.session.commit()
            return render_template("admin/batch/create_batch.html", courses=courses, students=students,
                                   msg="the batch has been registered", username = fetchusername())

        return render_template("admin/batch/create_batch.html", courses=courses, students=students, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")

@mod_site.route("/batch/delete/<batch_id>", methods=['GET'])
def delete_batch(batch_id):
    if session.get("user") and session.get("type") == "admin":
        from app.models.Batch import Batch
        from app.Blueprints import db

        b = Batch.query.get(batch_id)
        db.session.delete(b)
        db.session.commit()
    return redirect("/batch")

@mod_site.route("/batch/update/<batch_id>", methods = ["GET", "POST"])
def update_batch(batch_id):

    return ""

@mod_site.route("/batch/about/<batch_id>")
def aboutBatch(batch_id):
    if session.get("user") == True and session["type"] == "admin":
        from app.models.Course import Batch
        from app.Blueprints import db
        from app.models.Module import Module
        from app.models.Batch import Batch
        from app.models.Test import Test
        from app.models.Student import Student
        from app.models.Grades import Grades

        batch = Batch.query.get(batch_id)
        csv = "course,module,avg,max" + "\\n"
        maxMarks = 0
        for course in batch.courses:
            for module in course.modules:
                maxMarks = module.maxMarks
                for test in module.tests:
                    # find average grade
                    grades = list()
                    for i in test.grades:
                        grades.append(float(i.grade))
                    i = sum(grades)/len(grades)
                    csv = csv + str(course.name) + "," + str(module.name) + "," + str(float(i)) + "," + str(float(module.maxMarks)) + "\\n"


        return render_template("admin/batch/about.html", batch=batch, username = fetchusername(), csv=csv, maxMarks=maxMarks)



# tests

@mod_site.route("/test")
def accessTests():
    if session.get('user') == True and session['type'] == "admin":
        from app.models.Test import Test
        tests = Test.query.all()

        return render_template("admin/test/browse.html", tests=tests, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")


@mod_site.route("/test/new", methods=["GET", "POST"])
def createTest():
    if session.get("user") == True and session['type'] == "admin":
        from app.models.Batch import Batch
        batches = Batch.query.all()

        if request.method == "POST":
            from app.Blueprints import db
            from app.models.Test import Test
            from app.models.Student import Student
            from app.models.Module import Module
            from app.models.Grades import Grades



            newTest = Test(name = request.form.get("name"), date = request.form.get("date"), type = request.form.get("type"), module = request.form.get("module"))
            db.session.add(newTest)
            db.session.commit()
            StudentList = request.form.getlist("StudentList[]")
            for student in StudentList:
                stud = Student.query.get(student)
                grade = Grades(test_id=newTest.id, student_id=stud.id)
                newTest.grades.append(grade)
                stud.grades.append(grade)
                db.session.add(grade)
            db.session.commit()
            return render_template("admin/test/create_test.html", batches=batches, username = fetchusername())

        return render_template("admin/test/create_test.html", batches=batches, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")

@mod_site.route("/test/about/<id>")
def aboutTest(id):
    if session.get("user") == True and session["type"] == "admin":
        from app.Blueprints import db
        #students appearing in the test
        # general test details (date, type, graded)
        # if test graded then the grades of students who appeared in the test.
        # NOTE: if not graded, than the score is 0
        from app.models.Student import Student
        from app.models.Test import Test
        from app.models.Grades import Grades

        test = Test.query.get(id)
        students = []

        for grade in test.grades:
            student = Student.query.filter_by(id = grade.student_id)
            for stud in student:
                s = {
                    "id" : stud.id,
                    "name" : stud.fname+" "+stud.lname,
                    "grade" : grade.grade
                }
                students.append(s)
        return render_template("admin/test/about.html", test = test, students = students, username = fetchusername())
    else:
        return render_template("error/not_authorised.html")

@mod_site.route("/test/grade/<id>", methods = ["GET", "POST"])
def gradeTest(id):

    if session.get("user") == True and session['type'] == "admin":
        from app.Blueprints import db
        from app.models.Student import Student
        from app.models.Test import Test
        from app.models.Grades import Grades

        test = Test.query.get(id)
        studs = []

        for grade in test.grades:
            students = Student.query.filter_by(id = grade.student_id)

            for student in students:
                s = {
                    "id": student.id,
                    "name": student.fname + " " + student.lname,
                    "grade": grade.grade
                }
                studs.append(s)
        if request.method == "POST":
            grades = request.form.getlist("grades[]")
            for i in range(0, len(test.grades)):
                if(grades[i] == ''):
                    return render_template("admin/test/grading.html", students = studs, test = test, msg="dont keep marks field blank", username = fetchusername())
                test.grades[i].grade = float(grades[i])
            db.session.commit()
            link = "/test/grade/"+id
            return redirect(link)

        return render_template("admin/test/grading.html", students = studs, test = test, username = fetchusername())
    else:
        return render_template("errors/not_authorised.html")

@mod_site.route("/test/update/<id>", methods = ["GET", "POST"])
def updateTest(id):
    if session.get("user") == True and session["type"] == "admin":
        from app.Blueprints import db
        from app.models.Test import Test
        from app.models.Student import Student
        from app.models.Grades import Grades
        from app.models.Batch import Batch

        test = Test.query.get(id)
        batches = Batch.query.all()
        students = []
        for grade in test.grades:
            for stud in Student.query.filter_by(id = grade.student_id):
                students.append(stud.id)

        if request.method == "POST":
            for grade in test.grades:
                grade.query.delete()
            test.name = request.form.get("name")
            test.date = request.form.get("date")
            studentIds = request.form.getlist("StudentList[]")
            for sid in studentIds:
                student = Student.query.get(sid)
                grade = Grades(test_id = test.id, student_id = student.id)
                db.session.commit()
                test.grades.append(grade)
                student.grades.append(grade)
            test.type = request.form.get("type")
            db.session.commit()

            return redirect("/test")
    #students appearing in the test
    #test date

    return render_template("/admin/test/update.html", test = test, batches = batches, students = students, username = fetchusername())


def fetchusername():
    from app.Blueprints import db
    from app.models.Admin import Admin

    user = Admin.query.get(session['user'])
    return str(user.first_name + ' ' + user.last_name)
