import psycopg2
import psycopg2.extras
import sys
import pandas as psql

connection = psycopg2.connect("host='localhost' dbname='stock_data' user='James' password='i0cy7r9g'")

#list of functions for interacting with postgres database.

class database_methods(object):
    def __init__(self):
        print("just started")

    def main():
        try:
            #Define our connection string
            cursor = connection.cursor()
            print("Connecting to Database")
            cursor.execute("SELECT version()")
            ver = cursor.fetchone()
            print(ver)
        except psycopg2.DatabaseError as e:
            print ("Error '{0}'".format(e))
            sys.exit(1)

        finally:
            if conn:
                conn.close()
                print("Database Connection Closed")

    def table_create(self):
        try:
            cursor = connection.cursor()
            SQL = "CREATE TABLE {0} (Id BIGSERIAL PRIMARY KEY, Adj_Close FLOAT, Init_Close FLOAT, Close_Date DATE, High_P FLOAT, Low_P FLOAT , Open_P FLOAT , Symbol VARCHAR(8), Volume INT );".format(self)
            cursor.execute(SQL)
            conn.commit()
            print("Database Opened")
        except psycopg2.DatabaseError as e:
            print ("Error {0}", format(e))
            sys.exit(1)
        finally:
            if conn:
                conn.close()


    def write_database(self):
        try:
            cursor=connection.cursor()
            cursor.execute(self)
            conn.commit()
        except psycopg2.DatabaseError as e:
            print ("Error {0}", format(e))


    def read_database(self):
        try:
            cursor=connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(self)
            rows = cursor.fetchall()
            return rows
        except psycopg2.DatabaseError as e:
            print ("Error {0}", format(e))

    def pandas_read(self):
        #read database using pandas instead of direct connection. Way better
        #used this website: https://plot.ly/pandas/line-charts/
        dataframe = psql.read_sql(self,connection,index_col='id')
        return dataframe

    def close_database(self):
        conn = psycopg2.connect("host='localhost' dbname='stock_data' user='James' password='i0cy7r9g'")
        conn.close()
        print("Database Connection Closed")


if __name__ == "__main__":
	main()
