from app.models.Admin import Admin
from app.models.Attendance import Attendance
from app.models.Batch import Batch
from app.models.Course import Course
from app.models.Grades import Grades
from app.models.key import Key
from app.models.Module import Module
from app.models.Student import Student
from app.models.Subtest import Subtest
from app.models.Test import Test

from app.Blueprints import db

db.create_all()