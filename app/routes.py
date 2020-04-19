from flask import request
from app import app
from app.service import get_value, set_value, add_set, get_set, set_expiry, range_elements, rank

#End point for GET, SET and EXPIRE command
@app.route('/redis/key',methods=['POST','GET','PATCH'])
def keyDetails():
    if request.method == "GET":
        key = request.form['key']
        return get_value(key)
    elif request.method == "POST":
        key = request.form['key']
        value = request.form['value']
        return set_value(key,value)
    elif request.method == "PATCH":
        key = request.form['key']
        time = request.form['time']
        return set_expiry(key,time)
    else:
        return "bad request"

#End point for ZADD command
@app.route('/redis/set',methods=['POST', 'GET'])
def sorted_set():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
        score = request.form['score']
        return add_set(key,score,value)
    elif request.method == 'GET':
        return get_set()
    else:
        return "bad request"

#End point for ZRANGE command
@app.route('/redis/set/range',methods=['POST', 'GET'])
def range():
    if request.method == 'GET':
        key = request.form['key']
        left = request.form['left']
        right = request.form['right']
        return range_elements(key,left,right)
    else:
        return "bad request"

#End point for ZRANK command
@app.route('/redis/set/rank',methods=['POST', 'GET'])
def find():
    if request.method == 'GET':
        key = request.form['key']
        value = request.form['value']
        return rank(key,value)
    else:
        return "bad request"