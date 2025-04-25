from flask import g,Flask,render_template,request,redirect,url_for,render_template_string
import sqlite3
from datetime import datetime
from database import connect_db,get_db

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/', methods=['POST','GET'])
def index():
    db = get_db()
    
    if request.method == 'POST':
        date = request.form.get('date') #yyyy-mm-dd
        
        db_date = datetime.strptime(date,f'%Y-%m-%d')
        final_db_date = datetime.strftime(db_date, f'%Y%m%d')
        
        if_cur = db.execute('select entry_date from log_date where entry_date = ?',[final_db_date])
        if_result = if_cur.fetchone()
        if not if_result:
            db.execute('insert into log_date (entry_date) values (?);',[final_db_date])
            db.commit()
            return redirect(url_for('view_day',date=final_db_date))
        else:
            return redirect(url_for('view_day',date=final_db_date))
       
    
    
    cur = db.execute('''select log_date.entry_date, sum(food.protein) as protein, sum(food.carbohydrates) as carbohydrates, sum(food.fat) as fat, sum(food.calories) as calories from log_date 
                    left join food_date on food_date.log_date_id = log_date.id 
                    left join food on food.id = food_date.food_id group by log_date.id 
                    order by log_date.entry_date desc''')
    
    result = cur.fetchall()
    
    date_results = []
    for i in result:
        single_date = {}
        
        single_date['entry_date'] = i['entry_date']
        single_date['protein'] = i['protein']
        single_date['carbohydrates'] = i['carbohydrates']
        single_date['fat'] = i['fat']
        single_date['calories'] = i['calories']
        
        d = datetime.strptime(str(i['entry_date']), f'%Y%m%d')
        single_date['pretty_date'] = datetime.strftime(d,f'%B %d, %Y')
        date_results.append(single_date)

    
    
    return render_template('home.html',pretty_results=date_results)


@app.route('/view/<date>',methods=['POST','GET']) #yyyymmdd
def view_day(date):
    db = get_db()
    
    cur = db.execute('select * from log_date where entry_date = ?',[date])
    date_result = cur.fetchone()
    
    if request.method == 'POST':
        food_id = request.form.get('food-select')
        
        db.execute('insert into food_date (food_id,log_date_id) values(?,?)',[food_id,date_result['id']])
        db.commit()
    
    
    d = datetime.strptime(str(date_result['entry_date']), f'%Y%m%d')
    pretty_date = datetime.strftime(d, f'%B %d, %Y')
    
    food_cur = db.execute('select id, name from food')
    food_results = food_cur.fetchall()
    
    log_cur = db.execute('select food.name, food.protein, food.carbohydrates, food.fat, food.calories from log_date join food_date on food_date.log_date_id = log_date.id join food on food.id = food_date.food_id where log_date.entry_date = ?',[date])
    log_results = log_cur.fetchall()
    
    totals = {}
    totals['protein'] = 0
    totals['carbohydrates'] = 0
    totals['fat'] = 0
    totals['calories'] = 0
    
    for food in log_results:
        totals['protein'] += food['protein']
        totals['carbohydrates'] += food['carbohydrates']
        totals['fat'] += food['fat']
        totals['calories'] += food['calories']
        
        
    return render_template('day.html',
                           entry_date=date_result['entry_date'],
                           pretty_date=pretty_date,
                           food_results=food_results,
                           log_results=log_results,
                           totals=totals
                           )


@app.route('/food', methods=['GET','POST'])
def food():
    db = get_db()
    if request.method == 'POST':
        food_name = request.form.get('food-name')
        protein = int(request.form.get('protein'))
        carbohydrates = int(request.form.get('carbohydrates'))
        fat = int(request.form.get('fat'))
        #return render_template_string("<h2> {{ food_name }} {{ protein }} {{ carbs }} {{ fat }}</h2>",food_name=food_name,protein=protein,carbs=carbohydrates,fat=fat)
        calories = protein * 4 + carbohydrates * 4 + fat * 9
        
        if_cur = db.execute('select name from food where name = ?',[food_name])
        if_res = if_cur.fetchone()
        if not if_res:
            db.execute('insert into food (name,protein,carbohydrates,fat,calories) values(?,?,?,?,?);',[food_name,protein,carbohydrates,fat,calories])
            db.commit()
            return redirect(url_for('food'))
        else:
            return redirect(url_for('food'))
        
    
    cur = db.execute('select * from food;')
    results = cur.fetchall()
    
    return render_template('add_food.html',results=results)





























if __name__ == '__main__':
    app.run(debug=1)
    
    