import plotly
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import postgres
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np

#sign in credentials
#todo Hide these credentials


print("Plotly version: {0}".format(plotly.__version__))

#bunch of plotting functions using the plotly api

class get_data:
    def pull_date_price_data(self, start_date, end_date):
        #pulls date and closing price data for selected date range. Useful for a general plot of progress
        formatted_start_date = datetime.strptime(start_date.replace("-"," "), '%Y %m %d').date()
        formatted_end_date = datetime.strptime(end_date.replace("-"," "), '%Y %m %d').date()
        SQL="SELECT * FROM {0} WHERE close_date > '{1}' AND close_date <= '{2}';".format(self,formatted_start_date,formatted_end_date)
        data = postgres.database_methods.pandas_read(SQL)
        return data


class plot_graphs:
    #simple line of stock performance over time. Forms the basis for assessing the 'wealth' of the company
    def time_price_line(self, start_date, end_date):
        #put company data into a dataframe
        #from this website: https://plot.ly/pandas/line-charts/
        co1 = get_data.pull_date_price_data(self,start_date,end_date)
        #use column names to get column data and assign to axis
        x = co1['close_date']
        y = co1['adj_close']
        #put data into a dataframe - this is really where the magic happens
        df = pd.DataFrame({'x':x,'y':y})
        df.head()

        data=[
            Scatter(
                x=df['x'],
                y=df['y'],
                name = self
            )
        ]
        url = py.plot(data,filename='pandas/basic-line-plot')

    def two_comparison_price(self, company2, start_date,end_date):
        #comparison of two companies prices over time.
        #from this website: https://plot.ly/pandas/line-charts/
        co1 = get_data.pull_date_price_data(self, start_date,end_date)
        x = co1['close_date']
        y = co1['adj_close']
        df = pd.DataFrame({'x':x, 'y':y})
        df.head()

        co2 = get_data.pull_date_price_data(company2,start_date,end_date)
        x2 = co2['close_date']
        y2 = co2['adj_close']
        df2 = pd.DataFrame({'x':x2, 'y':y2})
        df2.head()

        data=[
            Scatter(
                x=df['x'],
                y=df['y'],
                name = self
            ),
            Scatter(
                x=df2['x'],
                y=df2['y'],
                name = company2
            )
        ]

        url = py.plot(data,filename='two-company-comparison')


