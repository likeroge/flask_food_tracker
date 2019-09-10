from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

def connec_db():
    sql = sqlite3.connect("D:\Progs\sqlite\food_log.db")
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite3_db = connec_db()
    return g.sqlite3_db

@app.teardown_appcontext
def close_db(err):
    if hasattr(g, 'sqlite3_db'):
        g.sqlite3_db.close()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/view")
def view():
   return render_template('day.html')

@app.route("/food")
def food():
    return render_template('add_food.html')

if __name__ == '__main__':
    app.run(debug=True)