from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
from datetime import datetime as dt   
import matplotlib.pyplot as plot

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('C:/Users/hp/Desktop/TestMyFoodDiary/Food_Diary/flask/database.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/addfood',methods = ['GET','POST'])
def addfood():
    db = get_db()
    if request.method == 'POST':
        request.method = 'GET'
        food_name = request.form['food_name']
        food_name = food_name.upper()
        curr = db.execute('select * from main_table where food_name = (?)',[food_name])
        rs = curr.fetchall()
        _date = dt.now()
        db.execute('insert into diet_table values(?,?,?,?,?,?,?,?)',
                        [rs[0]["food_name"],rs[0]["carbo"],rs[0]["protein"],rs[0]["fat"],
                        _date.strftime("%x"),_date.strftime("%d"),_date.strftime("%m"),_date.strftime("%Y")])
        db.commit()
    curr = db.execute('select food_name,carbo,protein,fat,_date from diet_table')
    rs = curr.fetchall()
    return render_template('listconsumedview.html',rs=rs)  
@app.route('/newfood', methods = ['GET','POST'])
def newfood():
    msg=''
    if request.method == 'POST':
        food_name = request.form.get('food_name')
        carbo = request.form.get('carbo')
        protein = request.form.get('protein')
        fat = request.form.get('fat')

        db = get_db()
        curr = db.execute('select * from main_table where food_name = ?', [food_name])
        existing_food = curr.fetchone()

        if existing_food:
            msg='This Food Item is already present!!..Try giving a new Food Item.'
        else:
            try:
                db.execute('INSERT INTO main_table VALUES (?, ?, ?, ?)', [food_name.upper(), carbo, protein, fat])
                db.commit()
                msg = 'Food Item is Successfully Added.'
            except Exception as e:
                msg = 'This Food Item is already present!!..Try giving a new Food Item.'
    return render_template('addfood.html', msg=msg)

@app.route('/updatefood', methods = ['GET','POST'])
def updatefood():
    if request.method == 'POST':
        food_name = request.form['food_name']
        db=get_db()
        db.execute('update main_table set carbo=?,protein=?,fat=? where food_name=?',[request.form['carbo'],
                    request.form['protein'],request.form['fat'],food_name])
        db.commit()
        db = get_db()
        curr = db.execute('select * from main_table')
        rs = curr.fetchall()
        return render_template('listview.html',rs=rs)
    else:
        food_name = request.args.get('food_name')
        if food_name:
            return render_template('updatefood.html', food_name=food_name)
    return render_template('listview.html', rs=rs)

@app.route('/deletefood', methods=['POST'])
def deletefood():
    if request.method == 'POST':
        food_name = request.form['food_name']
        db = get_db()
        db.execute('delete from main_table where food_name = ?', [food_name])
        db.commit()
    db = get_db()
    curr = db.execute('select * from main_table')
    rs = curr.fetchall()
    return render_template('listview.html',rs=rs)  

@app.route('/listview', methods = ['GET','POST'])
def listview():
    db = get_db()
    curr = db.execute('select * from main_table')
    rs = curr.fetchall()
    if request.method == 'POST':
        food_name=request.form['values.food_name']
        return redirect(url_for('updatefood',food_name=food_name))
    return render_template('listview.html',rs = rs)

@app.route('/listconsumedview')
def listconsumedview():
    db = get_db()
    curr = db.execute('select food_name,carbo,protein,fat,_date from diet_table')
    rs = curr.fetchall()
    return render_template('listconsumedview.html',rs = rs)

@app.route('/tracker')
def tracker():
    _date = dt.now()
    db = get_db()
    carbo1 = db.execute('select SUM(carbo) from diet_table WHERE (day = (?) AND month = (?) AND year = (?))',[_date.strftime("%d"),_date.strftime("%m"),_date.strftime("%Y")])
    cb1 = carbo1.fetchall()
    pro1 = db.execute('select SUM(protein) from diet_table WHERE (day = (?) AND month = (?) AND year = (?))',[_date.strftime("%d"),_date.strftime("%m"),_date.strftime("%Y")])
    po1 = pro1.fetchall()
    fat1 = db.execute('select SUM(fat) from diet_table WHERE (day = (?) AND month = (?) AND year = (?))',[_date.strftime("%d"),_date.strftime("%m"),_date.strftime("%Y")])
    ft1 = fat1.fetchall()

    carbo2 = db.execute('select SUM(carbo) from diet_table WHERE month = (?) AND year = (?)',[_date.strftime("%m"), _date.strftime("%Y")])
    cb2 = carbo2.fetchall()
    pro2 = db.execute('select SUM(protein) from diet_table WHERE month = (?) AND year = (?)',[_date.strftime("%m"), _date.strftime("%Y")])
    po2 = pro2.fetchall()
    fat2 = db.execute('select SUM(fat) from diet_table WHERE month = (?) AND year = (?)',[_date.strftime("%m"), _date.strftime("%Y")])
    ft2 = fat2.fetchall()

    carbo3 = db.execute('select SUM(carbo) from diet_table WHERE year = (?)',[_date.strftime("%Y")])
    cb3 = carbo3.fetchall()
    pro3 = db.execute('select SUM(protein) from diet_table WHERE year = (?)',[_date.strftime("%Y")])
    po3 = pro3.fetchall()
    fat3 = db.execute('select SUM(fat) from diet_table WHERE year = (?)',[_date.strftime("%Y")])
    ft3 = fat3.fetchall()
    return render_template('tracker.html',p1 = cb1,q1 = po1, r1 = ft1
                                         ,p2 = cb2,q2 = po2, r2 = ft2
                                         ,p3 = cb3,q3 = po3, r3 = ft3)

@app.route('/bargraph')
def bargraph():
    dat = dt.now()
    db = get_db()
    carbo1 = db.execute('select SUM(carbo) from diet_table WHERE day = (?)',[dat.strftime("%d")])
    cb1 = carbo1.fetchall()
    pro1 = db.execute('select SUM(protein) from diet_table WHERE day = (?)',[dat.strftime("%d")])
    po1 = pro1.fetchall()
    fat1 = db.execute('select SUM(fat) from diet_table WHERE day = (?)',[dat.strftime("%d")])
    ft1 = fat1.fetchall()
    c = str(cb1[0][0])
    p = str(po1[0][0])
    f = str(ft1[0][0])
    
    try:
        c = int(c)
        p = int(p)
        f = int(f)
    except:
        c=0
        p=0
        f=0

    x = ["sugg_C","cons_C"]
    y = [325,c]
    u = ["sugg_P","cons_P"]
    v = [56,p]
    a = ["sugg_F","cons_F"]
    b = [77,f]
    plot.bar(x,y,label="Carbohydrates")
    plot.bar(u,v,label="Proteins")
    plot.bar(a,b,label="Fats")
    plot.legend()
    plot.title("Bar Graph")
    plot.show()
    return render_template('home.html')

@app.route('/bargraph2')
def bargraph2():
    dat = dt.now()
    db = get_db()
    carbo2 = db.execute('select SUM(carbo) from diet_table WHERE year = (?)',[dat.strftime("%Y")])
    cb2 = carbo2.fetchall()
    pro2 = db.execute('select SUM(protein) from diet_table WHERE year = (?)',[dat.strftime("%Y")])
    po2 = pro2.fetchall()
    fat2 = db.execute('select SUM(fat) from diet_table WHERE year = (?)',[dat.strftime("%Y")])
    ft2 = fat2.fetchall()
    c1 = str(cb2[0][0])
    p1 = str(po2[0][0])
    f1 = str(ft2[0][0])
    
    try:
        c1 = int(c1)
        p1 = int(p1)
        f1 = int(f1)
    except:
        c1=0
        p1=0
        f1=0


    x = ["sugg_C","cons_C"]
    y = [9913,c1]
    u = ["sugg_P","cons_P"]
    v = [1708,p1]
    a = ["sugg_F","cons_F"]
    b = [2349,f1]
    plot.bar(x,y,label="Carbohydrates")
    plot.bar(u,v,label="Proteins")
    plot.bar(a,b,label="Fats")
    plot.legend()
    plot.title("Bar Graph(Month)")
    plot.show()
    return render_template('home.html')

@app.route('/bargraph1')
def bargraph1():
    dat = dt.now()
    db = get_db()
    carbo3 = db.execute('select SUM(carbo) from diet_table WHERE month = (?)',[dat.strftime("%m")])
    cb3 = carbo3.fetchall()
    pro3 = db.execute('select SUM(protein) from diet_table WHERE month = (?)',[dat.strftime("%m")])
    po3 = pro3.fetchall()
    fat3 = db.execute('select SUM(fat) from diet_table WHERE month = (?)',[dat.strftime("%m")])
    ft3 = fat3.fetchall()
    c2 = str(cb3[0][0])
    p2 = str(po3[0][0])
    f2 = str(ft3[0][0])
    
    try:
        c2 = int(c2)
        p2 = int(p2)
        f2 = int(f2)
    except:
        c2=0
        p2=0
        f2=0

    x = ["sugg_C","cons_C"]
    y = [118956,c2]
    u = ["sugg_P","cons_P"]
    v = [20496,p2]
    a = ["sugg_F","cons_F"]
    b = [28188,f2]
    plot.bar(x,y,label="Carbohydrates")
    plot.bar(u,v,label="Proteins")
    plot.bar(a,b,label="Fats")
    plot.legend()
    plot.title("Bar Graph(Year)")
    plot.show()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

