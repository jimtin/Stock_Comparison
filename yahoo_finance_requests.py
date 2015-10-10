import yahoo_finance
from yahoo_finance import Share
from datetime import datetime
import postgres

# this page is the main interaction page for program. Interacts with postgres.py

class pull_data:
    #class for pulling data from yahoo_finance. Ultimately the methods provide me a way to interact with a postgres database
    def __init__(self):
        return

    def stock_data(self):
        #function for assigning a stock symbol to a yahoo_finance method
        stock = Share(self)
        print(stock.get_open())

    def hist_data(self,start_date,end_date):
        #function for getting historical data about a stock from yahoo finance, releasing the example SQL to insert into db
        stock=Share(self).get_historical(start_date,end_date)
        for i in range(0, len(stock)):
            #SQL="Close was {0}, Open was {1}, Symbol is {2}".format(stock[i]['Close'],stock[i]['Open'],stock[i]['Symbol'])
            formatted_date = datetime.strptime(stock[i]['Date'].replace("-"," "), '%Y %m %d')
            print(formatted_date)
            SQL="INSERT INTO test_stock (adj_close, init_close, close_date,high_p,low_p,open_p,symbol,volume) VALUES ({0},{1},'{2}',{3},{4},{5},'{6}',{7});".format(stock[i]['Adj_Close'],stock[i]['Close'],formatted_date,stock[i]['High'],stock[i]['Low'],stock[i]['Open'],stock[i]['Symbol'],stock[i]['Volume'])
            print(SQL)

    def store_data(self,stock_code,start_date,end_date):
        #building on the hist_data function, this function stores the data into a postges db.
        stock=Share(stock_code).get_historical(start_date,end_date)
        postgres.database_methods.table_create(self)
        for i in range(0, len(stock)):
            #SQL="Close was {0}, Open was {1}, Symbol is {2}".format(stock[i]['Close'],stock[i]['Open'],stock[i]['Symbol'])

            #date must be formatted into correct type
            formatted_date = datetime.strptime(stock[i]['Date'].replace("-"," "), '%Y %m %d')
            SQL="INSERT INTO {8} (adj_close, init_close, close_date,high_p,low_p,open_p,symbol,volume) VALUES ({0},{1},'{2}',{3},{4},{5},'{6}',{7});".format(stock[i]['Adj_Close'],stock[i]['Close'],formatted_date,stock[i]['High'],stock[i]['Low'],stock[i]['Open'],stock[i]['Symbol'],stock[i]['Volume'],self)
            postgres.database_methods.write_database(SQL)
        postgres.database_methods.close_database('stock_data')




