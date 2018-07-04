import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__, static_folder="./site/static")
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from app.seed import *

from app.Blueprints.api.routes import mod_api
from app.Blueprints.site.routes import mod_site

app.register_blueprint(site.routes.mod_site)
app.register_blueprint(api.routes.mod_api, url_prefix = '/api')

def write_key(key):
    JSON_FILE = "{}/info.json".format(os.path.dirname(os.path.realpath(__file__)))
    with open(JSON_FILE, 'r') as jsonFile:
        data = json.load(jsonFile)
    data['lastcard'] = key
    jsonFile.close()

    with open(JSON_FILE, 'w') as jsonFile:
        json.dump(data, jsonFile)
    jsonFile.close()
    print("written")
    return True
