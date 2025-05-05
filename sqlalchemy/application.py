from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

#creates table (to make it, run "run4app")
class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #db.String(30) is getting mapped to varchar(30) in mysql
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    join_date = db.Column(db.DateTime)
    
    #the db.relationshop it is like creating the relationship in sqlalchemy
    #orders a virtual column in the other (Orders) table
    orders = db.relationship('Orders', backref='member', lazy='dynamic')
    #the backref means that a member can have multiple orders but the order can have 1 member
    courses = db.relationship('Course', secondary='user_courses', backref='member', lazy='dynamic')
    #so if i query an order, the .member would give me back the member_id
    #lazy is how the relationship is generated.
    
    
    #no need 4 constructor (only if i want something more than just assigning the value to the class attributes for example make instances)
    
    def __repr__(self):
        return f'Member({self.username},{self.password},{self.email},{self.join_date})'

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Integer)
    # @ Foreignkey('member.id') (yes member is in lowerspace) member is the class Member and the .id is the column (one to many) (this would be enough for the db relationship, but @ the member class i need to make a backref to make a realtionship in sqlalchemy too)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    
#if you dont need to manipulate the data in the table you dont need the class!!!!
#so instead of class:
db.Table('user_courses',
         db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
         db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
         )


if __name__ == '__main__':
    app.run(debug=True)