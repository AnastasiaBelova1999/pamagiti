import mysql.connector
from flask import g


class MySQL:
    def __init__(self, app):
        self.app = app
        self.app.teardown_appcontext(self.close_db)
        self.db = self.connect()

    def connection(self):
        if 'db' not in g:
            g.db = self.connect()
        return g.db

    def connect(self):
        return mysql.connector.connect(**self.config())

    def select(self, columns: list, table: str):
        try:
            if not isinstance(table, str):
                return False
            if columns is not None and not isinstance(table, str):
                return False
            sql_query: str = "SELECT "
            if columns is not None:
                for column in columns:
                    sql_query += "`" + str(column) + "`,"
                sql_query = sql_query[:-1]
            else:
                sql_query += "*"
            sql_query += " FROM " + "`" + table + "`"
            cursor = self.db.cursor(named_tuple=True)
            cursor.execute(sql_query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as error:
            print("mysql_db.select error")
            print(error)
            return False

    def where(self, table: str, name):
        if isinstance(table, str):
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM %s  WHERE name =\"%s\"' % (table, name))
            data = cursor.fetchall()
            cursor.close()
            return data
        else:
            return False

    def config(self):
        return {
            'user': self.app.config['MYSQL_USER'],
            'password': self.app.config['MYSQL_PASSWORD'],
            'host': self.app.config['MYSQL_HOST'],
            'database': self.app.config['MYSQL_DATABASE'],
        }

    def close_db(self, e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()