#!/usr/bin/env python
"""
Module to plot the data and generate the PNG image file
"""
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import sys
from optparse import OptionParser

INTERVAL = 2

def plot_data(db_file=None,
              column_names=None,
              image_file=None):
    """Function to plot the data in the database. Creates sub plots for
     the column names.
    """
    if not db_file:
        from . import config_pytomo
        db_file = config_pytomo.DATABASE_TIMESTAMP


    conn = sqlite3.connect(str(db_file),
                           detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    user_table = cur.execute('select name from sqlite_master '
                             'where type = "table"').fetchall()[0][0]
    fig = plt.figure (figsize=(10, 20))
    plt.suptitle('Pytomo: Youtube Download Statistics', color='brown',
                 size=16)
    fig.subplots_adjust(hspace=0.4)
    colors = ['red', 'green', 'brown', 'black', 'orange', 'cyan',
              'magenta' , 'blue', 'pink']
    colors *= 3
    print column_names
    for num, column_name in enumerate(list(column_names), 1):
        axes = fig.add_subplot(len(column_names), 1, num)
        fig.autofmt_xdate()
        dates = []
        cmd = ' '.join(("select strftime('%Y-%m-%d %H:%M:%S', ID),",
                            "AVG(", column_name, ")",
                            "from",
                            user_table,
                            "group by strftime('%Y%m%d%H%M',ID)"
                           ))
        cmd += "/" + str(INTERVAL) + ";"
        cur.execute(cmd)
        column_data = cur.fetchall()
        times_u, column_data = zip(*column_data)
        for _ in times_u:
            dates.append(datetime.datetime.strptime(_,
                                                '%Y-%m-%d %H:%M:%S'))
        try:
            axes.plot_date(dates, column_data, linestyle='-',
                       color=colors[num])
        except ValueError:
            print ''.join(("One of more columns have no numeric data",
                           "hence those columns have been skipped."))
            break
        date_fmt = mpl.dates.DateFormatter('%Hh%M')
        axes.xaxis.set_major_formatter(date_fmt)
        axes.set_ylabel(column_name)
        axes.grid(True)
        fig.savefig(image_file)
##    config_pytomo.LOG.info('The plot has been updated')


def create_options(parser):
    "Add the different options to parser"
    parser.add_option("-d", "--database", dest = "database",
                      help = " Sqlite database file_name")
    parser.add_option("-i", "--image_file", dest = "image_file",
                      default = "pytomo_graph.pdf",
                      help = "File to store output graphs (png or pdf)")
    parser.add_option("-T", "--DownloadTime", dest = "column_names",
                      action = 'append_const', default = None,
                      const = 'DownloadTime',
                      help = "Plot DownloadTime")
    parser.add_option("-V", "--VideoDuration", dest = "column_names",
                      const = 'VideoDuration',
                      action = 'append_const', default = None,
                      help = "Plot VideoDuration")
    parser.add_option("-L", "--VideoLength", dest = "column_names",
                      const = 'VideoLength',
                      action = 'append_const', default = None,
                      help = "Plot VideoLength")
    parser.add_option("-E", "--EncodingRate", dest = "column_names",
                      const = 'EncodingRate',
                      action = 'append_const', default = None,
                      help = "Plot EncodingRate")
    parser.add_option("-B", "--DownloadBytes", dest = "column_names",
                      const = 'DownloadBytes',
                      action = 'append_const', default = None,
                      help = "Plot DownloadBytes")
    parser.add_option("-I", "--DownloadInterruptions",
                      const = 'DownloadInterruptions',
                      dest = "column_names",
                      action = 'append_const', default = None,
                      help = "Plot DownloadInterruptions")
    parser.add_option("-F", "--BufferingDuration",
                      const = 'BufferingDuration',
                      action = 'append_const', default = None,
                      dest = "column_names",
                      help = "Plot BufferingDuration")
    parser.add_option("-P", "--PlaybackDuration",
                      const = 'PlaybackDuration',
                      action = 'append_const', default = None,
                      dest = "column_names",
                      help = "Plot PlaybackDuration")
    parser.add_option("-A", "--BufferDurationAtEnd",
                      dest = "column_names",
                      const = 'BufferDurationAtEnd',
                      action = 'append_const', default = None,
                      help = "Plot BufferDurationAtEnd")
    parser.add_option("-M", "--MaxInstantThp",
                      dest = "column_names",
                      const = 'MaxInstantThp',
                      action = 'append_const', default = None,
                      help = "Plot MaxInstantThp")
    parser.add_option("-m", "--PingMin",
                      dest = "column_names",
                      const = 'PingMin',
                      action = 'append_const', default = None,
                      help = "Plot PingMin")
    parser.add_option("-a", "--PingAvg",
                      dest = "column_names",
                      const = 'PingAvg',
                      action = 'append_const', default = None,
                      help = "Plot PingAvg")
    parser.add_option("-x", "--PingMax",
                      dest = "column_names",
                      const = 'PingMax',
                      action = 'append_const', default = None,
                      help = "Plot PingMax")

def main(argv=None):
    "Program wrapper"
    if argv is None:
        argv = sys.argv[1:]
    usage = ("%prog -d database | -g image_file [-T DownloadTime] "
            "[-V VideoDuration] [-L VideoLength]"
            " [-E EncodingRate] [-B DownloadBytes]"
            " [-I DownloadInterruptions]"
            " [-F BufferingDuration] [-P PlaybackDuration]"
            " [-A  BufferDurationAtEnd] [-M MaxInstantThp]"
            " [-m PingMin] [-a PingAvg] [-x PingMax]"
            "[-Y ALL COLUMNS]")
    parser = OptionParser(usage=usage)
    create_options(parser)
    (options, _) = parser.parse_args(argv)
    if not options.database:
        print ("Must provide database \n")
        parser.print_help()
        return(1)
    plot_data(db_file=options.database, column_names=options.column_names,
              image_file=options.image_file)

    print ''.join(("The plot for", str(options.column_names),
                 "from the database", options.database,
                 "has been saved to", options.image_file))


if __name__ == '__main__':
    sys.exit(main())


