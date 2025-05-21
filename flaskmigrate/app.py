from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    total = db.Column(db.Integer)

def create_app():
    
    app = Flask(__name__)
    
    #using /// is just saying it is in the current working directory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    #
    #migration process at the terminal: 
    #    flask db init
    #    flask db migrate  #  is going to compare the db that i have,
    #                      #  with the models that i have in the code, 
    #                      #  if it is any differences between the db and my class (Model), 
    #                      #  it will generate the code to match my classes and apply the changes to the database
    #to apply the changes:
    #   flask db upgrade
    # 
    #it is not always correct!!!!!
    #so check the generated code before upgrade @ migrations/versions
    #
    #the new db will be the /instance/[name]
    #
    #the 'flask db downgrade' will be downgrade the instance to the previous migrate
    #
    #
    
    return app