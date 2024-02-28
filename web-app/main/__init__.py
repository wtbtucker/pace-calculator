# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from flask import Flask
from .routes import main


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app