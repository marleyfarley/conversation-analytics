"""
Main module
- read data in from data/ directory
"""
"""
make the parsing flexible in case the format of text input
changes drastically. currently using 
https://github.com/PeterKaminski09/baskup to dump data
"""

#standard imports
import os
from math import pi
#module imports
from src.convo_objects.TextEquivalent import TextEquivalent
from src.calc_engine import metric_calculations as mc 
from src.read_parse import read_and_parse_text_file
from src.calc_engine import filter_poly as fil
from src.utilities import utils
from src.data_viz.visualize import create_volume_trends, create_time_trends
#plotting tings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from bokeh.io import gridplot, vplot, hplot
import bokeh.plotting as bkp
from bokeh.models import DatetimeTickFormatter
from bokeh.charts import Bar, output_file, show
import pandas as pd


###########################
## Read Data From File   ##
###########################
working_dir = os.getcwd()
data_folder = working_dir + os.sep + "data" 
text_file_name = "anon_convo.txt"
full_path = data_folder + os.sep + text_file_name

###########################
## Parse Data From File  ##
###########################

block_t_in_sec = 90
full_tes = read_and_parse_text_file(full_path,block_t_in_sec)
filt = fil.filter_by_day_of_week([1,2,3,4,5,6,7],full_tes)['filtered_tes']

###########################
## Calc Data From File  ##
###########################


r = mc.calculate_all_metrics(full_tes)

ub = utils.UtilityBoss()


s1_emojis = [ub.convert_emoji_code(code) for code in r['top_emojis_s1']]
s2_emojis = [ub.convert_emoji_code(code) for code in r['top_emojis_s2']]

r['top_emojis_s1'] = s1_emojis
r['top_emojis_s2'] = s2_emojis


#r2 = mc.calc_most_least_active_times(full_tes)
print(str(r))


zz = create_volume_trends(full_tes)

zzz = create_time_trends(full_tes)

output_file("main.html")


p_waits_hr = Bar(data=zzz['hours_df'],label='hour_x',group='participant',values='wait_time',
	title='Wait Times By Time of Day',legend='top_right',ylabel='Wait Time (sec)')

p_waits_day = Bar(data=zzz['days_df'],label='day_x',group='participant',values='wait_time',
	title='Wait Times By Day of Week',legend='top_right',ylabel='Wait Time (sec)')

p_emoji_hr = Bar(data=zzz['hours_df'],label='hour_x',group='participant',values='emoji_rate',
	title='Emoji Rate By Time of Day',legend='top_right',ylabel='Emoji Rate (%)')

p_emoji_day = Bar(data=zzz['days_df'],label='day_x',group='participant',values='emoji_rate',
	title='Emoji Rate By Day of Week',legend='top_right',ylabel='Emoji Rate (%)')

p_laugh_hr = Bar(data=zzz['hours_df'],label='hour_x',group='participant',values='laugh_rate',
	title='Laugh Rate (%) By Time of Day',legend='top_right',ylabel='Laugh Rate (%)')

p_laugh_day = Bar(data=zzz['days_df'],label='day_x',group='participant',values='laugh_rate',
	title='Laugh Rate (%) By Day of Week',legend='top_right',ylabel='Laugh Rate (%)')

p_dt_hr = Bar(data=zzz['hours_df'],label='hour_x',group='participant',values='double_text_rate',
	title='Double Text Rate (%) By Time of Day',legend='top_right',ylabel='Double Text Rate (%)')

p_dt_day = Bar(data=zzz['days_df'],label='day_x',group='participant',values='double_text_rate',
	title='Double Text Rate (%) By Day of Week',legend='top_right',ylabel='Double Text Rate (%)')

p_link_hr = Bar(data=zzz['hours_df'],label='hour_x',group='participant',values='link_rate',
	title='Link Rate (%) By Time of Day',legend='top_right',ylabel='Link Rate (%)')

p_link_day = Bar(data=zzz['days_df'],label='day_x',group='participant',values='link_rate',
	title='Link Rate (%) By Day of Week',legend='top_right',ylabel='Link Rate (%)')

p_curse_hr = Bar(data=zzz['hours_df'],label='hour_x',group='participant',values='curse_rate',
	title='Curse Rate (%) By Time of Day',legend='top_right',ylabel='Curse Rate (%)')

p_curse_day = Bar(data=zzz['days_df'],label='day_x',group='participant',values='curse_rate',
	title='Curse Rate (%) By Day of Week',legend='top_right',ylabel='Curse Rate (%)')




plot_volume_cumsum = bkp.figure(plot_width=500,plot_height=500,y_axis_label='Number of Text Equivalents')
plot_volume_cumsum.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
plot_volume_cumsum.xaxis.major_label_orientation = pi/4
plot_volume_cumsum.vbar(x=mdates.num2date(zz['x_ticks']),top=zz['cumsum'],width=0.1)

plot_volume = bkp.figure(plot_width=500,plot_height=500,y_axis_label='Number of Text Equivalents')
plot_volume.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
plot_volume.xaxis.major_label_orientation = pi/4
plot_volume.vbar(x=mdates.num2date(zz['x_ticks']),top=zz['y_vals'],width=0.1)

allplots = vplot(p_waits_hr,
				p_waits_day,
				plot_volume_cumsum,
				plot_volume,
				p_emoji_day,
				p_emoji_hr,
				p_laugh_hr,
				p_laugh_day,
				p_dt_day,
				p_dt_hr,
				p_link_hr,
				p_link_day,
				p_curse_hr,
				p_curse_day)
bkp.show(allplots)




