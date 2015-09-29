import yahoo_finance
from yahoo_finance import Share
from pprint import pprint
from datetime import datetime
import postgres


class pull_data:
    def __init__(self):
        return

    def stock_data(self):
        stock = Share(self)
        print(stock.get_open())

    def hist_data(self,start_date,end_date):
        stock=Share(self).get_historical(start_date,end_date)
        for i in range(0, len(stock)):
            #SQL="Close was {0}, Open was {1}, Symbol is {2}".format(stock[i]['Close'],stock[i]['Open'],stock[i]['Symbol'])
            formatted_date = datetime.strptime(stock[i]['Date'].replace("-"," "), '%Y %m %d')
            print(formatted_date)
            SQL="INSERT INTO test_stock (adj_close, init_close, close_date,high_p,low_p,open_p,symbol,volume) VALUES ({0},{1},'{2}',{3},{4},{5},'{6}',{7});".format(stock[i]['Adj_Close'],stock[i]['Close'],formatted_date,stock[i]['High'],stock[i]['Low'],stock[i]['Open'],stock[i]['Symbol'],stock[i]['Volume'])
            print(SQL)

    def store_data(self,stock_code,start_date,end_date):
        stock=Share(stock_code).get_historical(start_date,end_date)
        print(stock)
        postgres.database_methods.table_create(self)
        for i in range(0, len(stock)):
            #SQL="Close was {0}, Open was {1}, Symbol is {2}".format(stock[i]['Close'],stock[i]['Open'],stock[i]['Symbol'])
            formatted_date = datetime.strptime(stock[i]['Date'].replace("-"," "), '%Y %m %d')
            SQL="INSERT INTO {8} (adj_close, init_close, close_date,high_p,low_p,open_p,symbol,volume) VALUES ({0},{1},'{2}',{3},{4},{5},'{6}',{7});".format(stock[i]['Adj_Close'],stock[i]['Close'],formatted_date,stock[i]['High'],stock[i]['Low'],stock[i]['Open'],stock[i]['Symbol'],stock[i]['Volume'],self)
            print(SQL)
            postgres.database_methods.write_database(self,SQL)
        postgres.database_methods.close_database('stock_data')


