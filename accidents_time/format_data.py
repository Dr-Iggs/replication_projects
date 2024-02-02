# %%
import polars as pl
import pins
from lets_plot import *
LetsPlot.setup_html()
# %%
# dat = pl.read_csv("Motor_Vehicle_Collisions_-_Crashes_20240124.csv")\
#     .with_columns(
#         pl.col("CRASH DATE").str.to_date("%m/%d/%Y").alias("date"),
#         pl.col("CRASH TIME").str.to_time("%H:%M").alias("time"),
#         pl.concat_str(["CRASH DATE","CRASH TIME"], separator=" ")\
#             .str.to_datetime("%m/%d/%Y %H:%M").alias("date_time"))

# dat.write_parquet("ny_crashes.parquet", compression="zstd", compression_level=15)
# %%
dat = pl.read_parquet("ny_crashes.parquet")

#%%
day_hours = dat.with_columns(Date_Hour = pl.col('date_time').dt.truncate('1h')) \
    .group_by('Date_Hour') \
    .agg(Accidents=pl.col('Date_Hour').count(),
         Deaths = (pl.col('NUMBER OF PEDESTRIANS KILLED')+pl.col('NUMBER OF PERSONS KILLED')).sum(),
         Injuries=(pl.col('NUMBER OF PEDESTRIANS INJURED')+pl.col('NUMBER OF PERSONS INJURED')).sum())

# %%
# Now we want to create two visuals: the number of chrashes per hour and one that shows the number of injuries per day
timeline = day_hours.with_columns(Day_Month=pl.col('Date_Hour').dt.truncate('1w'))\
    .group_by(pl.col('Day_Month'))\
    .agg([pl.col('Injuries').sum(),
          pl.col('Accidents').count()])\
    .melt(id_vars='Day_Month')\
    .sort(pl.col('Day_Month'))

ggplot(timeline,aes(x='Day_Month',y='value',group='variable')) +\
    geom_path()

# %%
import polars as pl
from lets_plot import *
LetsPlot.setup_html()
ratio = day_hours.with_columns(Hour=pl.col('Date_Hour').dt.hour()) \
    .group_by('Hour') \
    .agg(Accidents=pl.col('Accidents').sum(),
        Injuries=pl.col('Injuries').sum(),
        Deaths=pl.col('Deaths').sum())\
    .sort('Hour') \
    .with_columns(Ratio=((pl.col('Deaths')*100) / (pl.col('Deaths')+pl.col('Injuries'))))

ggplot(ratio,aes(y='Ratio',x='Hour')) + geom_path() +\
    scale_y_continuous(breaks=[0.5,1,1.5,1.9],labels=['.5%','1%','1.5%','1.9%']) +\
    scale_x_continuous(breaks=[0,6,12,18],labels=['Midnight','6am','Noon','6pm']) +\
    labs(x='Time of Day',y='Percentage of all injuries that are fatal',
         title='Night crashes are more likely to be deadly')
# %%
