from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__, static_folder="./site/static")
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

engine = create_engine("mysql+pymysql://admin:Admin_2k18@172.104.181.210:3306/cafelingua")
connection = engine.connect()
if connection:
    print("works")

from app.Blueprints.api.routes import mod_api
from app.Blueprints.site.routes import mod_site

app.register_blueprint(site.routes.mod_site)
app.register_blueprint(api.routes.mod_api, url_prefix = '/api')
