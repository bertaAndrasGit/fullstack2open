from flask import Flask
#i use flask Flask-Reuploaded, not Flask-Uploads, because it is not maintained, this is a drop-in replacement,which means it is the same code without the werkzeug error.
from flask_uploads import configure_uploads
from .routes import pages,photos,docs






def create_app():

    app = Flask(__name__)
    
    

    #after the UPLOADED_ i need to use the name of the UploadSet that i created.
    app.config['UPLOADED_PHOTOS_DEST'] = 'pictures'
    app.config['UPLOADED_PHOTOS_ALLOW'] = ['txt','pdf']
    #app.config['UPLOADED_PHOTOS_DENY'] = ['py','php','c']
    app.config['UPLOADS_DEFAULT_DEST'] = 'other'
    app.register_blueprint(pages) 
    #a register blueprints után kell!!!!!
    configure_uploads(app, (photos,docs))
      
    
    return app