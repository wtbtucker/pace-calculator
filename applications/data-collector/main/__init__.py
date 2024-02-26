# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from extensions import db
from flask import Flask
from routes import data_collector

def create_app(database_url='postgresql://postgres:postgres@localhost/weather'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # with app.app_context():
    #     db.create_all()

    db.init_app(app)
    app.register_blueprint(data_collector)
    return app
