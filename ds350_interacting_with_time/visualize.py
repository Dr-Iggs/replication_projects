# %%
import polars as pl
import pandas as pd

import plotly.graph_objects as go
from datetime import datetime
from lets_plot import *
LetsPlot.setup_html()

# %%
pdat = pl.read_parquet("stock.parquet")

# %%
# Create a time series chart that shows performance of all 10 stocks.
from datetime import datetime
year_ticks = [datetime(2019, 1, 1, 0, 0),
              datetime(2020, 1, 1, 0, 0),
              datetime(2021, 1, 1, 0, 0),
              datetime(2022, 1, 1, 0, 0),
              datetime(2023, 1, 1, 0, 0),
              datetime(2024, 1, 1, 0, 0)]

ggplot(pdat,aes(x='date',y='Open',group='ticker',color='ticker')) +\
    geom_path() +\
    scale_x_continuous(breaks=year_ticks,labels=['2019','2020','2021','2022','2023']) +\
    labs(x='Date',y='Daily Open Price',title='10 Stocks over 5 Years')
# %%

ggplot(pdat.filter(pl.col('ticker')=='GM'),aes(x='date',group='ticker',color='ticker',y='Volume')) +\
    geom_path(aes(linewidth='Volume')) +\
    scale_x_continuous(breaks=year_ticks,labels=['2019','2020','2021','2022','2023'])
    
# now fix the html size and only show the last year and save the chart
#%%
pdat = pdat.with_columns(DailyDrop=pl.col('Open')-pl.col('Close')) \
            .with_columns(PosNeg=pl.when(pl.col('DailyDrop')>0).then(pl.lit('Positive')).otherwise(pl.lit('Negative')))
ggplot(pdat.filter(pl.col('ticker')=='WDAY'),aes(x='Volume',y='DailyDrop',color='PosNeg')) +\
    geom_point() +\
    scale_color_manual(values={'Positive':'green','Negative':'red'}) +\
    scale_x_log10() +\
    labs(x='Number of Stocks traded',y='Change by the end of the day',title='5 years of daily changes for GM',
         subtitle='Prices shift the most on high-trade days')
# %%
## plotly candlestick chart
# https://plotly.com/python/candlestick-charts/

import plotly.graph_objects as go

go.Figure(data=[go.Candlestick(x=pdat['date'],open=pdat['Open'],high=)])

#%%

yearly = pdat.with_columns(Year= pl.col('date').dt.year()) \
                           .group_by('Year','ticker') \
        .agg(price=pl.col('Close').mean()) \
        .sort('Year')


ggplot(yearly,aes(x='Year',y='price',group='ticker',color='ticker')) +\
    geom_path() +\
    labs(x='Date',y='Daily Open Price',title='10 Stocks over 5 Years')
