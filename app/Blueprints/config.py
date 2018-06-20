import os
DEBUG = True
#live server

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://cafelingua:__DEEPAK@172.104.181.210/cafelingua"
#local server
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "hbe9pZqXWyLaHbjw07d3KRAbM4d3G9Af"

JSON_FILE = "{}/info.json".format(os.path.dirname(os.path.realpath(__file__)))

# setup mailing server
