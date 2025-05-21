from flask import Flask,render_template
from flask_mail import Mail,Message

def create_app():
    app = Flask(__name__)
    # how to set up gmail: https://support.google.com/mail/answer/7126229?visit_id=638830970690227784-3301553669&hl=hu&rd=1
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'example@gmail.com'
    app.config['MAIL_PASSWORD'] = 'password'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = ('Andrew','example@gmail.com')
    
    
    #this will help, because sometimes email servers won't allow to send too many 
    #messages, so it vill close the connection after 5 eamil and reopens it, so the 
    #'with mail.connect() as conn:' can continue the queue.
    app.config['MAIL_MAX_EMAILS'] = 5
    
    
    mail = Mail()
    mail.init_app(app)    
    
    @app.route('/')
    def index():
        msg = Message('Hello from Flask!',recipients=['plsscrape@me.com','example@msn.com'])
        msg.add_recipient = 'example@yahoo.com'
        #msg.body = 'Plain text'
        msg.html = '<h3>This is a HTML message</h3>'
        
        #the open_resource allows to open op a file in the project
        with app.open_resource('flask_cheatsheet.pdf') as pdf:
            #the second param. is from here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types
            msg.attach('this_is_the_name_param.pdf','application/pdf',pdf.read())
        
        mail.send(msg)
        
        return '<h1>Sent!</h1>'
    
    @app.route('/bulk')
    def bulk():
        users = [{'name':'Andras','email':'andras@email.com'}]
        
        with mail.connect() as conn:
            for user in users:
                msg = Message('Bulk',recipients=[user['email']])
                msg.body = f'Hello {user["name"]}'
                conn.send(msg)

    
    
    
    return app