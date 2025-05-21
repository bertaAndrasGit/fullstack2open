from flask import Flask,render_template,Blueprint
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,PasswordField, IntegerField, BooleanField, Form, FormField, FieldList
from wtforms.validators import InputRequired, Length,AnyOf,NumberRange, Email
from flaskwtforms.formclasses import LoginForm,User,NameForm,DynamicForm
from collections import namedtuple

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

@pages.route('/',methods=['GET','POST'])
def index():
    #current_user = User(email='john@example.com',username='Johnn')
    #print('BEFORE')
    #print(current_user.email)
    #print(current_user.username)
    #print('\n')
    #form = NameForm(obj=current_user)
    
    group = namedtuple('Group',['year','total'])
    g1 = group(2015, 5000)
    g2 = group(2017, 5000)
    g3 = group(2019, 5000)
    g4 = group(2021, 5000)
    g5 = group(2025, 5000)
    
    data = {'years':[g1, g2, g3, g4, g5]}
    
    form = NameForm(data=data)
    
    #delete the mobile_phone formfields
    del form.mobile_phone
    
    if form.validate_on_submit():
        #form.populate_obj(current_user)
        #print('AFTER')
        #print(current_user.email)
        #print(current_user.username)
        #print('\n')
        
        output = '<h1>'
        
        for field in form.years:
            output += f'Year: {field.year.data} '
            output += f'Total: {field.total.data} <br />'
            
        output += '</h1>'
        
        return output
        
        
        
        #return f'Country Code: {form.mobile_phone.country_code.data} Area Code: {form.home_phone.area_code.data} Number: {form.home_phone.number.data}'
        #return f"<h1>Email: {form.email.data} Username: {form.username.data} Password: {form.password.data} Age: {form.age.data} Yes: {form.yesorno.data}</h1>"
    
    return render_template('index.html',form=form)


@pages.route('/dynamic',methods=['GET','POST'])
def dynamic():
    
    
    
    #we can make the form in the index route "dynamically"
    DynamicForm.name = StringField('name')
    DynamicForm.password = PasswordField('password')
    
    names = ['middle_name','last_name','nickname']
    
    for name in names:
        setattr(DynamicForm,name,StringField(name))
    
    form = DynamicForm()
    
    
    if form.validate_on_submit():
         #datetime.date
        return f'<h3> Dynamic!!!!! <br /> Name: {form.name.data} <br /> Password: {form.password.data}</h3>'
    
    
    return render_template('dynamic.html',form=form,names=names)

