"""App central."""
from flask import Flask

from Products.extensions import configuration, views


def create_app():
    """."""
    app = Flask(__name__)
    configuration.init_app(app)
    views.init_app(app)
    return(app)
