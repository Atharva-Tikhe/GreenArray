import mysql.connector


class DbConnection:
    def __init__(self, user, passwd, db, table):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.table = table
        self.conn = mysql.connector.connect(host='localhost', user = self.user, passwd = self.passwd, db = self.db)
        # conn = mysql.connector.connect(host='localhost', user = 'root', passwd = 'GA_db_1234', db = 'nbs')
        return self.conn
        