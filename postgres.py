import psycopg2
import sys
import pprint

class database_methods(object):
    def __init__(self):
        print("just started")

    def main():
        try:
            #Define our connection string
            conn = psycopg2.connect("host='localhost' dbname='James' user='James' password='i0cy7r9g'")
            cursor = conn.cursor()
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

    def table_create(tablename):
        print(tablename)
        try:
            conn = psycopg2.connect("host='localhost' dbname='James' user='James' password='i0cy7r9g'")
            print("Table Name: {0}".format(tablename))
            cursor = conn.cursor()
            SQL = "CREATE TABLE {0} (Id INTEGER PRIMARY KEY, Adj_Close FLOAT, Init_Close FLOAT, Close_Date DATE, High_P FLOAT, Low_P FLOAT , Open_P FLOAT , Symbol VARCHAR(8), Volume INT );".format(tablename)
            print(SQL)
            cursor.execute(SQL)
            conn.commit()
        except psycopg2.DatabaseError as e:
            print ("Error {0}", format(e))
            sys.exit(1)
        finally:
            if conn:
                conn.close()
                print("Database Connection Closed")

    def write_database(self, SQL):
        try:
            conn = psycopg2.connect("host='localhost' dbname='{0}' user='James' password='i0cy7r9g'".format(self))
            print("Database Opened")
            cursor=conn.cursor()
            cursor.execute(SQL)
            conn.commit()
        except psycopg2.DatabaseError as e:
            print ("Error {0}", format(e))
            sys.exit(1)
        finally:
            if conn:
                conn.close()
                print("Database Connection Closed")


if __name__ == "__main__":
	main()
