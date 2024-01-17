import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'GA_db_1234', db = 'nbs')


df = pd.read_csv('./processed.tsv', delimiter='\t', header=0)

def push_to_db():
    engine = create_engine("mysql+mysqlconnector://root:Tikheatharva#22@localhost/nbs")
    df.to_sql('variants', engine, 'nbs', if_exists='replace')
    # df.to_json('webapp/data/data.json')

push_to_db()

