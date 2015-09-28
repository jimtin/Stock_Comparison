import re, sys, os, time,datetime, csv
import pandas
import sqlite3 as lite
from yahoo_finance_historical_data_extract import YFHistDataExtr
from Yahoo_finance_YQL_company_data import YComDataExtr


#import stock data. Code found: https://simplypython.wordpress.com/2015/03/04/storing-and-retrieving-stock-data-from-sqlite-database/
class FinanceDataStore(object):
    def __init__(self, db_full_path):
        self.con=lite.connect(db_full_path)
        self.cur=self.con.cursor()
        self.hist_data_tablename='histprice'
        #use for datekeys
        self.set_data_limit_datekey = ''
        #output data
        self.hist_price_df=pandas.DataFrame()

    def close_db(self):
        self.con.close()

    def break_list_to_sub_list(self, full_list,chunk_size=45):
        """ Break list into smaller equal chunks specified by chunk_size.
            Args:
                full_list (list): full list of items.
            Kwargs:
                chunk_size (int): length of each chunk.
            Return
                (list): list of list.
        """
        if chunk_size < 1:
            chunk_size=1
        return [full_list[i:i + chunk_size] for i in range(0, len(full_list), chunk_size)]

    def setup_db_for_hist_prices_storage(self,stock_sym_list,interval):
        #get price history
        histdata_extract = YFHistDataExtr()
        histdata_extract.set_interval_to_retrieve(360*interval)
        histdata_extract.enable_save_raw_file=0
        for sub_list in self.break_list_to_sub_list(stock_sym_list):
            print ('processing sub list', sub_list)
            histdata_extract.set_multiple_stock_list(sub_list)
            histdata_extract.get_hist_data_of_all_target_stocks()
            histdata_extract.removed_zero_vol_fr_dataset()
            # save to SQL table
            histdata_extract.processed_data_df.to_sql(self.hist_data_tablename, self.con, flavor='sqlite',
                                    schema=None, if_exists='append', index=True,
                                    index_label=None, chunksize=None, dtype=None)

        self.close_db()

    def break_list_to_sub_list(self,full_list, chunk_size = 45):
        """ Break list into smaller equal chunks specified by chunk_size.
            Args:
                full_list (list): full list of items.
            Kwargs:
                chunk_size (int): length of each chunk.
            Return
                (list): list of list.
        """
        if chunk_size < 1:
            chunk_size = 1
        return [full_list[i:i + chunk_size] for i in range(0, len(full_list), chunk_size)]

    def setup_db_for_hist_prices_storage(self, stock_sym_list):
        """ Get the price and dividend history and store them to the database for the specified stock sym list.
            The length of time depends on the date_interval specified.
            Connection to database is assuemd to be set.
            For one time large dataset (where the hist data is very large)
            Args:
                stock_sym_list (list): list of stock symbol.

        """

        ## set the class for extraction
        histdata_extract = YFHistDataExtr()
        histdata_extract.set_interval_to_retrieve(360*5)# assume for 5 years information
        histdata_extract.enable_save_raw_file = 0

        for sub_list in self.break_list_to_sub_list(stock_sym_list):
            print ('processing sub list', sub_list)
            histdata_extract.set_multiple_stock_list(sub_list)
            histdata_extract.get_hist_data_of_all_target_stocks()
            histdata_extract.removed_zero_vol_fr_dataset()

            ## save to one particular funciton
            #save to sql -- hist table
            histdata_extract.processed_data_df.to_sql(self.hist_data_tablename, self.con, flavor='sqlite',
                                    schema=None, if_exists='append', index=True,
                                    index_label=None, chunksize=None, dtype=None)

            #save to sql -- div table
            histdata_extract.all_stock_div_hist_df.to_sql(self.divdnt_data_tablename, self.con, flavor='sqlite',
                                    schema=None, if_exists='append', index=True,
                                    index_label=None, chunksize=None, dtype=None)

        self.close_db()

    def scan_and_input_recent_prices(self, stock_sym_list, num_days_for_updates = 10 ):
        """ Another method to input the data to database. For shorter duration of the dates.
            Function for storing the recent prices and set it to the databse.
            Use with the YQL modules.
            Args:
                stock_sym_list (list): stock symbol list.
            Kwargs:
                num_days_for_updates: number of days to update. Cannot be set too large a date.
                                    Default 10 days.

        """

        w = YComDataExtr()
        w.set_full_stocklist_to_retrieve(stock_sym_list)
        w.set_hist_data_num_day_fr_current(num_days_for_updates)
        w.get_all_hist_data()

        ## save to one particular funciton
        #save to sql -- hist table
        w.datatype_com_data_allstock_df.to_sql(self.hist_data_tablename, self.con, flavor='sqlite',
                                schema=None, if_exists='append', index=True,
                                index_label=None, chunksize=None, dtype=None)

    def retrieve_stocklist_fr_db(self):
        """ Retrieve the stocklist from db
            Returns:
                (list): list of stock symbols.
        """
        command_str = "SELECT DISTINCT SYMBOL FROM %s "% self.hist_data_tablename
        self.cur.execute(command_str)
        rows = self.cur.fetchall()

        self.close_db()
        return [n[0].encode() for n in rows]

    def retrieve_hist_data_fr_db(self, stock_list=['CBA.AX'], select_all =1):
        """ Retrieved a list of stocks covering the target date range for the hist data compute.
            Need convert the list to list of str
            Will cover both dividend and hist stock price
            Kwargs:
                stock_list (list): list of stock symbol (with .SI for singapore stocks) to be inputted.
                                    Will not be used if select_all is true.
                select_all (bool): Default to turn on. Will pull all the stock symbol

        """
        stock_sym_str = ''.join(['"' + n +'",' for n in stock_list])
        stock_sym_str = stock_sym_str[:-1]
        #need to get the header
        command_str = "SELECT * FROM %s where symbol in (%s)"%(self.hist_data_tablename,stock_sym_str)
        if select_all: command_str = "SELECT * FROM %s "%self.hist_data_tablename
        self.cur.execute(command_str)
        headers =  [n[0] for n in self.cur.description]

        rows = self.cur.fetchall() # return list of tuples
        self.hist_price_df = pandas.DataFrame(rows, columns = headers) #need to get the header?? how to get full data from SQL

        ## dividend data extract
        command_str = "SELECT * FROM %s where symbol in (%s)"%(self.divdnt_data_tablename,stock_sym_str)
        if select_all: command_str = "SELECT * FROM %s "%self.divdnt_data_tablename

        self.cur.execute(command_str)
        headers =  [n[0] for n in self.cur.description]

        rows = self.cur.fetchall() # return list of tuples
        self.hist_div_df = pandas.DataFrame(rows, columns = headers) #need to get the header?? how to get full data from SQL

        self.close_db()

    def add_datekey_to_hist_price_df(self):
        """ Add datekey in the form of yyyymmdd for easy comparison.

        """
        self.hist_price_df['Datekey'] = self.hist_price_df['Date'].map(lambda x: int(x.replace('-','') ))

    def extr_hist_price_by_date(self, date_interval):
        """ Limit the hist_price_df by the date interval.
            Use the datekey as comparison.
            Set to the self.hist_price_df

        """
        self.add_datekey_to_hist_price_df()
        target_datekey = self.convert_date_to_datekey(date_interval)
        self.hist_price_df = self.hist_price_df[self.hist_price_df['Datekey']>=target_datekey]

    def convert_date_to_datekey(self, offset_to_current = 0):
        """ Function mainly for the hist data where it is required to specify a date range.
            Default return current date. (offset_to_current = 0)
            Kwargs:
                offset_to_current (int): in num of days. default to zero which mean get currnet date
            Returns:
                (int): yyymmdd format

        """
        last_eff_date_list = list((datetime.date.today() - datetime.timedelta(offset_to_current)).timetuple()[0:3])

        if len(str(last_eff_date_list[1])) == 1:
            last_eff_date_list[1] = '0' + str(last_eff_date_list[1])

        if len(str(last_eff_date_list[2])) == 1:
            last_eff_date_list[2] = '0' + str(last_eff_date_list[2])

        return int(str(last_eff_date_list[0]) + last_eff_date_list[1] + str(last_eff_date_list[2]))