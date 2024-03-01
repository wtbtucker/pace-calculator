# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from extensions import db
from flask import Flask
from DataCollectorRoutes import data_collector_bp

def create_app(database_url='postgres://weather_0kgp_user:EKj5lznn7a8MkhWfFyLoRtKtAUXbUmbS@dpg-cnh0aoicn0vc73fcl7c0-a/weather_0kgp'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    db.init_app(app)

    create_tables=os.getenv('CREATE_TABLES', False)
    if create_tables:
        with app.app_context():
            db.create_all()

    
    app.register_blueprint(data_collector_bp)
    return app
