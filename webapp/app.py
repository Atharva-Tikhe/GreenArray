import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import mysql.connector

load_dotenv('./webapp/project.env')

app = Flask(__name__)

conn = mysql.connector.connect(host='localhost', user = 'root', passwd = os.getenv('PASS'), db = 'nbs')
curs = conn.cursor(buffered=True)



@app.route('/')
def send_index():
    return render_template('index.html')


@app.route('/get_headers')
def send_db_headers():
    curs.execute('select * from variants;')
    return jsonify(curs.column_names)

@app.route('/process_query/<geno>', methods = ['POST', 'GET'])
def send_result(geno):
    print("This is flask")
    print(geno)
    curs.execute(f'select * from variants where `allele_ratio` = {geno}')
    res = curs.fetchall()
    res.insert(0, curs.column_names)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)