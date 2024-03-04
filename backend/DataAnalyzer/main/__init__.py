import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from extensions import db
from flask import Flask
from DataAnalyzerRoutes import data_analyzer_bp, get_forecast

def create_app(database_url='postgresql://postgres:postgres@db:5432/weather'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    db.init_app(app)
    app.register_blueprint(data_analyzer_bp)

    return app