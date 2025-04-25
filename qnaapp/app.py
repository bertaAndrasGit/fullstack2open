from flask import Flask, render_template,g,request,redirect,url_for,render_template_string,session
from database import connect_db, get_db
from werkzeug.security import generate_password_hash,check_password_hash
import os
import functools
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
#print(app.config['SECRET_KEY'])

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

def get_current_user():
    user_result = None
    
    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute('select id,name,password,expert,admin from users where name = ?',[user])
        user_result = user_cur.fetchone()
    
    return user_result

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args,**kwargs):
        user = session.get('user')
        if user is None:
            return redirect(url_for("login"))
        
        return route(*args,**kwargs)
    
    return route_wrapper

def admin_required(route):
    @functools.wraps(route)
    def route_wrapper(*args,**kwargs):
        user = get_current_user()
        if user['admin'] == 0:
            return redirect(url_for("index"))
        
        return route(*args,**kwargs)
    
    return route_wrapper

def expert_required(route):
    @functools.wraps(route)
    def route_wrapper(*args,**kwargs):
        user = get_current_user()
        if user['expert'] == 0:
            return redirect(url_for("index"))
        
        return route(*args,**kwargs)
    
    return route_wrapper






@app.route('/')
@login_required
def index():
    user = get_current_user()
    db = get_db()
    questions = db.execute('select id, question_text, (select name from users where questions.expert_id = id) as expert_name, (select name from users where questions.asked_by_id = id) as asker_name from questions where answer_text is not null').fetchall()
    
    return render_template('home.html',user=user,questions=questions)


@app.route('/register',methods=['GET','POST'])
def register():
    user = get_current_user()
    db = get_db()
    
    if request.method == 'POST':
        
        existing_user = db.execute('select id from users where name = ?',[request.form.get('name')]).fetchone()
        
        if existing_user:
            return render_template('register.html',user=user, error='User already exists!')
        
        hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256:600000', salt_length=16)
        db.execute('insert into users (name,password,expert,admin) values (?,?,?,?)',[request.form.get('name'),hashed_password, '0', '0'])
        db.commit()
        
        session['user'] = request.form.get('name')
        
        return redirect(url_for('index'))

    
    return render_template('register.html',user=user)


@app.route('/login',methods=["GET","POST"])
def login():
    user = get_current_user()
    db = get_db()

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
        user_cur = db.execute('select id,name,password from users where name = ?',[name])
        user_result = user_cur.fetchone()
        
        if user_result:
            if check_password_hash(user_result['password'],password):
                session['user'] = user_result['name']
                return redirect(url_for('index'))
            else:
                return render_template('login.html',user=user, error='Username or password is incorrect!')
        return render_template('login.html',user=user, error='Username or password is incorrect!')
        
    return render_template('login.html',user=user)


@app.route('/question/<question_id>')
@login_required
def question(question_id):
    user = get_current_user()
    db = get_db()
    
    question = db.execute('select id, question_text, answer_text, (select name from users where questions.expert_id = id) as expert_name, (select name from users where questions.asked_by_id = id) as asker_name from questions where id = ?',[question_id]).fetchone()
    
    
    
    return render_template('question.html',user=user,question=question)


@app.route('/answer/<question_id>',methods=['GET','POST'])
@login_required
@expert_required
def answer(question_id):
    user = get_current_user()
    db = get_db()
    
    if request.method == 'POST':
        answer_text = request.form.get('answerText')
        db.execute('update questions set answer_text = ? where id = ?',[answer_text,question_id])
        db.commit()
        
        return redirect(url_for('unanswered'))
    
    question = db.execute('select id, question_text from questions where id = ?',[question_id]).fetchone()
    
    return render_template('answer.html',user=user,question=question)


@app.route('/ask',methods=['GET','POST'])
@login_required
def ask():
    db = get_db()
    user = get_current_user()
    
    if request.method == "POST":   
        question = request.form.get('question')
        expert = request.form.get('expert')
        db.execute('insert into questions (question_text,asked_by_id,expert_id) values (?,?,?)',[question,user['id'],expert])
        db.commit()
        return redirect(url_for('index'))
    
    
    expert_cur = db.execute('select id, name from users where expert = 1')
    expert_res = expert_cur.fetchall()
        
    
    return render_template('ask.html',user=user,expert_res=expert_res)


@app.route('/unanswered')
@login_required
@expert_required
def unanswered():
    user = get_current_user()
    db = get_db()
    
    questions = db.execute('select id, question_text, (select name from users where questions.asked_by_id = id) as asker_name from questions where answer_text is null and expert_id = ?',[user['id']]).fetchall()
    
    return render_template('unanswered.html',user=user,questions=questions)


@app.route('/users')
@login_required
@admin_required
def users():
    db = get_db()
    user = get_current_user()
    
    user_cur = db.execute('select id,name,expert,admin from users')
    user_res = user_cur.fetchall()
    
    return render_template('users.html',user=user,user_res=user_res)


@app.route('/logout')
@login_required
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))


@app.get('/promote/<user_id>') #a user id-t stringként kapom meg
@login_required
@admin_required
def promote(user_id):
    db = get_db()
    
    expert_cur = db.execute('select id from users where expert = 1')
    who_expert = expert_cur.fetchall()
    
    print([expert["id"] for expert in who_expert])

    if int(user_id) in [expert["id"] for expert in who_expert]:
        db.execute('UPDATE users SET expert = 0 where id = ?',[user_id])
    else:
        db.execute('UPDATE users SET expert = 1 where id = ?',[user_id])
       
    db.commit()
    return redirect(url_for('users'))



















if __name__ == '__main__':
    app.run(debug=True)