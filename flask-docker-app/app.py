from flask import jsonify, json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database="to_do_list",
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            port=5430)
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM lists;')
    lists = cur.fetchall()
    cur.close()
    conn.close()
    
    listItems = []
    
    for i in lists:
        listDict = {
        'id': i[0],
        'item': i[1]}
        listItems.append(listDict)
    
    print(listItems)
    return jsonify(listItems)

@app.route('/list/', methods=['GET', 'POST'])
def list_index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lists")
    lists = cur.fetchall()
    cur.close()
    conn.close()
    
    listItems = []
    
    for i in lists:
        listDict = {
        'id': i[0],
        'item': i[1]}
        listItems.append(listDict)
        
    return jsonify(listItems)

@app.route('/search/<string:item>/', methods=['GET', 'POST'])
def search_list_item(item):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lists WHERE item LIKE %s ESCAPE '';",(item,))
    lists = cur.fetchall()
    cur.close()
    conn.close()
    
    listItems = []
    
    for i in lists:
        listDict = {
        'id': i[0],
        'item': i[1]}
        listItems.append(listDict)
        
    return jsonify(listItems)
    
@app.route('/add/<string:item>/', methods=['GET', 'POST'])
def add_list_item(item):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO lists (item)'
            'VALUES (%s);',
            (item,))
    conn.commit()
    cur.close()
    conn.close()
    
    add_result = {
        'result': "Success",
        }
        
    return jsonify(add_result)

app.run()