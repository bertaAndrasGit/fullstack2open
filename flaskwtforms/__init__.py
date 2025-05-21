from flask import Flask,render_template
import os
from dotenv import load_dotenv
from .routes import pages

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'secret'
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY') or 'secret'
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600 #seconds
    app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    app.config['TESTING'] = True
    
    
    app.register_blueprint(pages)
    return app


