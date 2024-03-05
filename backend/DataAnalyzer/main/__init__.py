import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from extensions import db
from flask import Flask
from DataAnalyzerRoutes import data_analyzer_bp

def create_app(database_url='postgresql://weather_0kgp_user:EKj5lznn7a8MkhWfFyLoRtKtAUXbUmbS@dpg-cnh0aoicn0vc73fcl7c0-a/weather_0kgp'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    db.init_app(app)
    app.register_blueprint(data_analyzer_bp)

    return app