from flask import Flask,g,request,jsonify
import sqlite3
from database import connect_db,get_db
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)

def protected(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth = request.authorization
        if auth and auth.username == os.environ.get("API_USERNAME") and auth.password == os.environ.get("API_PASSWORD"):
            return f(*args,**kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

    

@app.route('/member',methods=['GET'])
@protected
def get_members():
    db = get_db()
    
    
    if request.method == "GET":
        members = db.execute('select id,name,email,level from members').fetchall()
        json = []
        for member in members:
            member_dict = {}
            member_dict["id"] = member["id"]
            member_dict["name"] = member["name"]
            member_dict["email"] = member["email"]
            member_dict["level"] = member["level"]
            json.append(member_dict)
        
    
    return jsonify({"members":json})
    


@app.route('/member/<int:member_id>',methods=['GET'])
@protected
def get_member(member_id):
    db = get_db()
    
    if request.method == "GET":
        member = db.execute('select id,name,email,level from members where id = ?',[member_id]).fetchone()
        
        
    
    return jsonify(
                { "member":
                    {"id":member["id"],
                    "name":member["name"],
                    "email":member["email"],
                    "level":member["level"]}
                }
                   )


@app.route('/member',methods=['POST'])
@protected
def add_member():
    db = get_db()
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    if request.method == "POST":
        db.execute('insert into members (name,email,level) values (?,?,?)',[name,email,level])
        db.commit()
        
        member = db.execute('select id,name,email,level from members where email = ?',[email]).fetchone()
        
    return jsonify(
                    {"id":member["id"],
                    "name":member["name"],
                    "email":member["email"],
                    "level":member["level"]}
                   )


@app.route('/member/<int:member_id>',methods=['PUT','PATCH'])
@protected
def edit_member(member_id):
    db = get_db()
    new_member_data = request.get_json()
    
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    
    if request.method == "PUT" or request.method == "PATCH":
        db.execute('UPDATE members set name = ?,email = ?,level = ? where id = ?',[name,email,level,member_id])
        db.commit()
        
        updated_member = db.execute('select id,name,email,level from members where id = ?',[member_id]).fetchone()
        
        updated_member_json = {}
        updated_member_json["id"] = updated_member["id"]
        updated_member_json["name"] = updated_member["name"]
        updated_member_json["email"] = updated_member["email"]
        updated_member_json["level"] = updated_member["level"]

    
    return jsonify({"updated member": updated_member_json})


@app.route('/member/<int:member_id>',methods=['DELETE'])
@protected
def delete_member(member_id):
    db = get_db()
    if request.method == "DELETE":
        db.execute('DELETE FROM members where id = ?',[member_id])
        db.commit()
    
    return jsonify(f'DELETED member whos id was #{member_id}')








if __name__ == '__main__':
    app.run(debug=True)