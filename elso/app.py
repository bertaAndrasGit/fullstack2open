from flask import Flask,jsonify,render_template_string,request,url_for,redirect,session


app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = '[mygeneratedsecretkey]'

@app.route("/",methods=['GET','POST'], defaults= {'name': 'Jojo'})
def index(name):
    return f'<h1>Something... {name}</h1>'


@app.route("/home",methods=['GET','POST'], defaults= {'name': 'Default'})
@app.route("/home/<name>",methods=['GET','POST'])
def home(name):
    #make a session var.
    session['name'] = name
    return render_template_string('<h1>Hi, {{ name }}</h1>',name=name)

@app.route("/json")
def json():
    #read a session var.
    #if there is nothing at the 'name' key, a key error will po pup! (to see this error we need to clear the session and we need to delet the default params at the home route) 
    #so we need to make it like this
    if 'name' in session:
        name = session['name']
    else:
        name = 'NOTINSESSION'
        
    return jsonify([{'key':'value','key2':[1,2,3,4,5]},{'key1':'value1','key12':{'value12':'valuevalue12'}},{'name': name}])


@app.route('/query')
def query():
    name = request.args.get('name')
    location =  request.args.get('location')
    #example: http://127.0.0.1:5000/query?name=Sarah&location=Hawaii
    return render_template_string("<h1>Hi, {{ name }} from {{ location}}! You're in the Query page!</h1>",name=name,location=location)


@app.route('/theform')
def theform():
    return '''
              <form method="POST" action="/process">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit" value='Submit'>
              </form>
            '''
@app.route('/process',methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    
    return render_template_string('<p> Hello {{ name }} from {{ location }}! You have submitted the form <strong>successfully!</strong></p>',name=name,location=location)


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    
    return jsonify({'Result' : 'Success!', 'name': name, 'location': location, 'randomkeylist': randomlist[1]})


@app.route('/getpost',methods=['GET','POST'])
def getpost():
    
    if request.method == 'GET':
         return '''
              <form method="POST" action="/getpost">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit" value='Submit'>
              </form>
                '''
    else:
        name = request.form['name']
        location = request.form['location']
        
        # return render_template_string(
        #     """
        #     <p> Hello {{ name }} from {{ location }}! 
        #     You have submitted the form 
        #     <strong>successfully!</strong></p>
        #     """,
        #     name=name,location=location)
        return redirect(url_for('home', name=name, location=location))
    
    