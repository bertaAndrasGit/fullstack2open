from flask import Flask
from .views import demo

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aintnothinggonnabreakmystride'

    app.register_blueprint(demo)

    return app