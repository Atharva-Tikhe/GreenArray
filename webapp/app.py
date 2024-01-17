import os
# from dotenv import load_dotenv
import mysql.connector
from flask import Flask, render_template, request, jsonify, flash, redirect, session
from flask_session import Session
from werkzeug.utils import secure_filename
import pandas as pd
from sqlalchemy import create_engine

# load_dotenv('./webapp/project.env')

# File handling conditions
UPLOAD_FOLDER = 'webapp/webapp/samples/'
ALLOWED_EXTENSIONS = {'tsv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


conn = mysql.connector.connect(host=os.environ['MYSQL_HOST'], user = os.environ['MYSQL_USER'], passwd = os.environ['MYSQL_PASSWORD'], db = os.environ['MYSQL_DB'])
# Keep buffered on to send all the records at once 
curs = conn.cursor(buffered=True)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def send_index():
  ref_df = pd.read_csv('webapp/webapp/processed_56878_v1-full_wc.tsv', sep='\t')
  engine = create_engine(f"mysql+mysqlconnector://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DB']}")
  ref_df.to_sql('variants', engine, 'nbs', if_exists='replace')
  return render_template('index.html')

@app.route('/get_all')
def send_db_headers():
    curs.execute('select * from variants;')
    return jsonify(curs.column_names)

@app.route('/process_query/<query>/<category>', methods = ['POST', 'GET'])
def send_result(query, category):
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

# File input handling, store in samples dir 
@app.route('/fileInput', methods = ['GET', 'POST'])
def get_file():
    if request.method == 'POST' and request.form.get('gender') != None:
    # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            from match_in_db import MatchWithDb
            obj = MatchWithDb('webapp/webapp/processed_56878_v1-full_wc.tsv', filepath, request.form.get('gender'))
            common_entries = obj.common
            styler = common_entries.style
            styler.set_table_styles([
                {"selector": "tr", "props": "line-height: 12px;"},
                {"selector": "td,th", "props": "line-height: inherit; padding: 0;"}
                ])
            # return render_template('uploadResponse.html', commons = common_entries)
            return f'<html><body>{common_entries.to_html(columns=["# locus", "type", "ref", "genotype", "allele_frequency_%", "zygosity" ,"entry_count"],classes="table table-stripped")}</body></html>'
    else:
        return 'Error'

if __name__ == '__main__':
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(host='0.0.0.0',port=8080, debug=True)