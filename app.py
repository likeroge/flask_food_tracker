from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime


app = Flask(__name__)


def connect_db():
    sql = sqlite3.connect(
        '/home/egor/Документы/Programming/Python/DB/food_log.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/", methods=['POST', 'GET'])
def index():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date']  # YYYY-MM-DD format
        print(date)

        dt = datetime.strptime(date, '%Y-%m-%d')
        print(dt)
        database_date = datetime.strftime(dt, '%Y%m%d')
        print(database_date)

        db.execute('insert into log_date (entry_date) values (?)',
                   [database_date])
        db.commit()

    cursor = db.execute(
        'select entry_date from log_date order by entry_date desc')
    print(cursor)
    results = cursor.fetchall()
    print(results)
    pretty_results = []

    for i in results:
        print(i)
        single_date = {}
        d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        print(d)
        single_date['entry_date'] = datetime.strftime(d, '%B %d, %Y')
        print(single_date)
        pretty_results.append(single_date)

    return render_template('home.html', results=pretty_results)


@app.route('/view/<date>', methods=['GET', 'POST'])
def view(date):
    if request.method=='POST':
        return f"<h1>The food Item added is #{request.form['food-select']}</h1>"
    db = get_db()
    cursor = db.execute('select entry_date from log_date where entry_date = ?', [date])
    result = cursor.fetchone()
    
    d = datetime.strptime(str(result['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(d, '%B %d, %Y')

    food_cursor = db.execute('select id, name from food')
    food_results = food_cursor.fetchall()

    return render_template('day.html', date = pretty_date, food_results = food_results)


@app.route("/food", methods=['GET', 'POST'])
def food():
    db = get_db()
    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])

        calories = protein*4+carbohydrates*+fat*9

        db.execute('insert into food (name, protein, carbohydrate, fat, calories) values (?, ?, ?, ?, ?)', [
                   name, protein, carbohydrates, fat, calories])
        db.commit()

    cursor = db.execute(
        'select name, protein, carbohydrate, fat, calories from food')
    results = cursor.fetchall()

    return render_template('add_food.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
