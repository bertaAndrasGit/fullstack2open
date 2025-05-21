from flask import Blueprint,render_template,request

from flask_uploads import UploadSet,IMAGES,UploadNotAllowed,TEXT
pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)



#it allows to upload only image files
photos = UploadSet('photos', IMAGES)
docs = UploadSet('docs', TEXT)

#we can combine the TEXT and IMAGES and odd more to it.add()
stuff = UploadSet('wow',TEXT + IMAGES + ('py','php','cpp'))
@pages.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST' and 'thefile' in request.files:
        
        try:
            image_filename = photos.save(request.files['thefile'])
            #docs_filename = docs.save(request.files['thefile'])
            return f'<h1>{image_filename}</h1>'
        except UploadNotAllowed:
            return'<h1>Format not allowed</h1>'
    
    
    return render_template('upload.html')