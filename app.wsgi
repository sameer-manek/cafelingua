import sys

sys.path.insert(0, "/sites/cafelingua")

from app import app as application
#from app import manager

application.debug = True
