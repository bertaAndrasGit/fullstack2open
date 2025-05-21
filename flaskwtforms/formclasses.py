from flask import Flask,render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField, IntegerField, BooleanField, Form, FormField, FieldList, ValidationError, DateField
from wtforms.validators import InputRequired, Length,AnyOf,NumberRange, Email
from dataclasses import dataclass,field


class TelephoneForm(Form):
    country_code= IntegerField('country code')
    area_code = IntegerField('area code')
    number = StringField('number')
    
#inherits from form, not flaskform, because we will use it in flaskform
class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')
    
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[Email()])
    username = StringField('username',validators=[InputRequired(),Length(min=5,max=10,message='Between 5 and 10 please!')])
    password = PasswordField('password',validators=[InputRequired(),AnyOf(values=['secret','password','pass'])])
    age = IntegerField('age', validators=[NumberRange(min=18,max=100,message='Between 18 and 100 please!')])
    yesorno = BooleanField('yes or no?',validators=[])
    
    
class NameForm(LoginForm):
    first_name = StringField('first name')
    last_name = StringField('last name')
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    
    #we can give parameters with the fieldlist
    years = FieldList(FormField(YearForm),min_entries=5)
    recaptcha = RecaptchaField('recaptcha')

    #custom "inline" validator (must start the func name with validate_)
    def validate_first_name(form,field):
        if field.data != 'Andrew':
            raise ValidationError('You dont have the right name!')
    
class DynamicForm(FlaskForm):
    #need to match the standard datetime.date format
    #YYYY-MM-DD
    entrydate = DateField('entry date',format='%Y-%m-%d')


@dataclass
class User():
    email:str
    username:str
    password:str = field(default='pass')
    age:int = field(default=25)
    yesorno:bool = field(default=True)
    