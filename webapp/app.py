import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import mysql.connector


load_dotenv('./webapp/project.env')
app = Flask(__name__)


conn = mysql.connector.connect(host='localhost', user = 'root', passwd = os.getenv('PASS'), db = 'nbs')
curs = conn.cursor(buffered=True)



@app.route('/')
def send_index():
    return render_template('index.html')


@app.route('/get_all')
def send_db_headers():
    curs.execute('select * from variants;')
    return jsonify(curs.column_names)

@app.route('/process_query/<query>/<category>', methods = ['POST', 'GET'])
def send_result(query, category):
    print("This is flask")
    print(query)
    print(category)
    if category == 'locus':
        curs.execute(f'select * from variants where `# locus` = {query}')
        res = curs.fetchall()
        res.insert(0, curs.column_names)
        return jsonify(res)
    else:
        curs.execute(f'select * from variants where `{category}` = {query}')
        res = curs.fetchall()
        res.insert(0, curs.column_names)
        return jsonify(res)
        

if __name__ == '__main__':
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    # Session(app)
    app.run(port=8080, debug=True)