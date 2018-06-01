import sys

sys.path.insert(0, "/sites/cafelingua")

from app import app as application

application.debug = True