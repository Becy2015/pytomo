# Introduction #

Pytomo is a Python based tomographic tool to perform analysis of video download
rates on websites that provide video streaming services: actually `YouTube` and `Dailymotion` are implemented.

# Usage #

## Video crawl ##
```
start_crawl.py [-r max_rounds] [-u max_crawled_url] [-p max_per_url]
[-P max_per_page] [-t time_frame] [-s {youtube, dailymotion}][-n ping_packets]
[-D download_time] [-B buffering_video_duration] [-M min_playout_buffer_size]
[-x] [-L log_level] [-R] [input_urls]
```

```
    Options:
  -h, --help            show this help message and exit
  -r MAX_ROUNDS         Max number of rounds to perform (default 10000)
  -l, --loop            Loop after completing the max nb of rounds
  -u MAX_CRAWLED_URL    Max number of urls to visit (default 10000)
  -p MAX_PER_URL        Max number of related urls from each page (default 20)
  -P MAX_PER_PAGE       Max number of related videos from each page (default
                        20)
  -t TIME_FRAME         Timeframe for the most popular videos to fetch at
                        start of crawl put 'today', 'week', 'month' or
                        'all_time' (default 'week')
  -s CRAWL_SERVICE      Service for the most popular videos to fetch at start
                        of crawl: select between 'youtube', or 'dailymotion'
                        (default 'youtube')
  -n PING_PACKETS       Number of packets to be sent for each ping (default
                        10)
  -D DOWNLOAD_TIME      Download time for the video in seconds (default
                        30.000000)
  -B INITIAL_PLAYBACK_DURATION 
                        Buffering video duration in seconds (default
                        2000.000000)
  -M MIN_PLAYOUT_BUFFER_SIZE
                        Minimum Playout Buffer Size in seconds (default
                        0.100000)
  -x                    Do NOT store public IP address of the machine in the
                        logs
  -L LOG_LEVEL          The log level setting for the Logging module.Choose
                        from: 'DEBUG', 'INFO', 'WARNING', 'ERROR' and
                        'CRITICAL' (default 'DEBUG')
  --http-proxy=PROXIES  in case of http proxy to reach Internet (default None)
  --provider=PROVIDER   Indicate the ISP
  -R, --no-related      Do NOT crawl related videos (stays with the first urls
                        found: either most popular or arguments given)
```

## Graphical web interface ##
```
start_server.py [-v] [-f database] [-d database_directory] [port]
```

```
Options:
  -h, --help            show this help message and exit
  -v, --verbose         run as verbose mode
  -f DB_NAME, --file=DB_NAME
                        run on a specific database (by default the latest
                        database in the default database directory is
                        selected)
  -d DB_DIR_NAME, --dir=DB_DIR_NAME
                        run on a specific directory where the latest database
                        will be selected
```


# Installation-free #

In order to provide installation-free package, we provide binary stand-alone
**executables for Windows** (32 bits). The binaries files were generated with Pyinstaller (version 1.5RC1).<br>

If you have Python installed, you can directly run the 'start_crawl.py' script at<br>
root or the pytomo script in bin directory.<br>
<pre><code>    python start_crawl.py<br>
</code></pre>

If you have Python installed and the RRDtool python bindings, you can<br>
directly run the 'start_server.py' script at root - you may to specify a port<br>
on which to start the server and then connect to that port on the respective<br>
host from your favourite browser. By default, the graphical web<br>
interface will run on port 5555:<br>
<pre><code>    python start_server.py<br>
</code></pre>
You will then connect on the respective machine (you need to know its IP and<br>
make sure it allows external connections, otherwise you will only be able to<br>
see the graphs locally on that machine):<br>
<blockquote><a href='http://localhost:5555/'>http://localhost:5555/</a> or <a href='http://127.0.0.1:5555/'>http://127.0.0.1:5555/</a>          <= visualisation on local machine<br>
<a href='http://192.168.1.18:5555/'>http://192.168.1.18:5555/</a>      <= visualisation from remote host (inside a local network in this example)</blockquote>

By default, the graphs are collected with information from the latest database<br>
in the default database directory. If a new live crawl is started, it is<br>
recommended to stop and start again the graphical web interface and refresh the<br>
page from your browser.<br>
<br>
<h1>External Resources</h1>

The <code>RRDtool</code> python binding necessary for the graphical web interface should<br>
be installed from the repository of your OS distribution:<br>
- For Debian based OS:<br>
<pre><code>    sudo apt-get install python-rrdtool<br>
</code></pre>
- For RHEL based OS:<br>
<pre><code>    yum install python-rrdtool<br>
</code></pre>

The library for YouTube downloads is based on the <code>youtube_dl</code> script.<br>
<br>
The dns module is taken from the <code>DNS Python Package</code>: we just modified rdata<br>
so that <code>Pyinstaller</code> includes all needed modules.<br>
<br>
The extraction of metadata out of video files is an adaptation of `Kaa Metadata<br>
Python Package`: it has been modified in order to be independent of Kaa-base<br>
(thus pure Python and portable).<br>
<br>
The web server necessary for the graphical web interface is based on <code>web.py</code>
that is included in the Pytomo distribution sources.<br>
<br>
<h2>External Links</h2>

<ol><li><code>YouTube Download</code>: <a href='http://rg3.github.com/youtube-dl/'>http://rg3.github.com/youtube-dl/</a>
</li><li><code>Kaa Metadata Python Package</code>: <a href='http://packages.debian.org/sid/python-kaa-metadata'>http://packages.debian.org/sid/python-kaa-metadata</a>
</li><li><code>DNS Python Package</code>: <a href='http://pypi.python.org/pypi/dnspython'>http://pypi.python.org/pypi/dnspython</a>
</li><li><code>Pyinstaller</code>: <a href='http://www.pyinstaller.org/'>http://www.pyinstaller.org/</a>
</li><li><code>RRDtool</code>: <a href='http://oss.oetiker.ch/rrdtool/'>http://oss.oetiker.ch/rrdtool/</a>
</li><li><code>web.py</code>: <a href='http://webpy.org/'>http://webpy.org/</a>