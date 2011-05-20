#!/usr/bin/env python
"""
Module to plot the data and generate the PNG image file
"""
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
from . import config_pytomo

INTERVAL = 2

def plot_data(db_file=config_pytomo.DATABASE_TIMESTAMP,
              image_file=None):
    """Function to plot the data in the database. Creates sub plots for
     Download Interruptions, Buffering Duration, Playback Duration,
    """
    conn = sqlite3.connect(str(db_file), detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    user_table = cur.execute('select name from sqlite_master '
                             'where type = "table"')
    cmd = ' '.join(("select strftime('%Y-%m-%d %H:%M:%S', ID),",
                    "AVG(", "DownloadInterruptions", "),",
                    "AVG(", "BufferingDuration", "),",
                    "AVG(", "PlaybackDuration", "),",
                    "AVG(", "DownloadBytes/1000", "),",
                    "AVG(", "MaxInstantThp", ")",
                    "from",
                    user_table.fetchall()[0][0],
                    "group by strftime('%Y%m%d%H%M',ID)"
                   ))
    cmd += "/" + str(INTERVAL) + ";"
    cur.execute(cmd)
    all_results = cur.fetchall()
    times_u, dwn_int, buff_dur, play_bck_dur, dwn_bytes, max_inst_thrp = zip(
        *all_results)
    dates = []
    for time_val in times_u:
        dates.append(datetime.datetime.strptime(time_val, '%Y-%m-%d %H:%M:%S'))
    fig = plt.figure(1, figsize=(10, 10))
    plt.suptitle('Pytomo: Youtube Download Statistics', color='brown', size=16)
    fig.autofmt_xdate()
    fig.subplots_adjust(hspace=0.4)
    axes = fig.add_subplot(411)
    axes.plot_date(dates, dwn_bytes, linestyle='-')
    date_fmt = mpl.dates.DateFormatter('%Hh%M')
    axes.xaxis.set_major_formatter(date_fmt)
    axes.set_ylabel('Downloaded Bytes(Kb)', color='blue')
    axes.grid(True)

    axes = fig.add_subplot(412)
    axes.plot_date(dates, buff_dur, linestyle='-', color='green')
    date_fmt = mpl.dates.DateFormatter('%Hh%M')
    axes.xaxis.set_major_formatter(date_fmt)
    axes.set_ylabel('Buffering Duration', color='green')
    axes.grid(True)

    axes = fig.add_subplot(413)
    axes.plot_date(dates, play_bck_dur, linestyle='-', color='brown')
    date_fmt = mpl.dates.DateFormatter('%Hh%M')
    axes.xaxis.set_major_formatter(date_fmt)
    axes.set_ylabel('Playback Duration', color='brown')
    axes.grid(True)

    axes = fig.add_subplot(414)
    axes.plot_date(dates, max_inst_thrp, linestyle='-', color='orange')
    date_fmt = mpl.dates.DateFormatter('%Hh%M')
    axes.xaxis.set_major_formatter(date_fmt)
    axes.set_ylabel('MaxInstantThp', color='Orange')
    axes.grid(True)

    fig.savefig(image_file)
    config_pytomo.LOG.info('The plot has been updated')

