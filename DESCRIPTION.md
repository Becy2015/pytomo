# PYTOMO #

  * Authors: Louis Plissonneau, Parikshit Juluri, Mickaël Meulle (Orange Labs)
  * Research Collaborators: Ernst Biersack (Eurecom), Deep Medhi (UMKC)
  * Version: 0.4.0
  * Email : pytomo@gmail.com
  * Copyright: GPLv2

**Table of Contents**


# Description #

Pytomo is a Python based tomographic tool to perform analysis of Youtube video download rates. We first select an initial list of videos that we would like to start the analysis with. For the videos in this list the Pytomo tool first finds the IP address of the cache servers on which these videos are located. The cache server is pinged to obtain the RTT times. Then we try to download the video for a limited amount of time to calculate the different statistics of the download.


# Usage of the files #

## Setup.py ##

The setup file used to create the python package.

## DESCRIPTION.txt ##

This file in RestructuredText.

## start\_crawl.py ##

This is the global launcher for the Pytomo tool.

## pytomo/ ##

This folder contains the pytomo package. The contents of it are listed below.

### start\_pytomo.py ###


The top-most module that is used to run the Pytomo tool.

#### Usage ####
> Terminal:
```
        python start_pytomo.py
```
> Interactive python:
```
        import start_pytomo.main
        import config_pytomo
        start_pytomo.main()
```
#### Functions ####

  * **compute\_stats(url)** Returns a list of the statistics related to the url. The contents of the list are : (url, cache\_url, current\_stats) where current\_stats is a list containing: `[`Ping\_times, download\_statistics, DNS resolver used `]`

  * **format\_stats(stats)** Functions used to format the stats obtained from compute\_stats function so that they can be inserted into the sqlite3 database. The stats are converted into a tuple. The arguments to this function is the list returned by compute\_stats().

  * **md5\_sum(input\_file)** Function to generate the standard md5 of the file. Done to cope with the large file values taken from Python distribution.

  * **check\_out\_files(filepattern, directory, timestamp)** Returns a full path of the file used for the output. It checks if the path exists, if not then the file is created in the path if possible else it is created in the default user directory.

  * **do\_crawl(result\_stream=sys.stdout, db\_file=None, timestamp=None)** Crawls the urls given by the urlfile.txt(present in the package). The crawl is performed upto MAX\_ROUNDS or MAX\_VISITED\_URLS. The statistical results obtained are inserted into the db\_file.

  * **main(argv=None)** This is the program wrapper for the start\_pytomo module. It is mainly used to setup and initialize the logging and other startup parameters.

### config\_pytomo.py ###


File containing the various parameters and constants that are used for the analysis. The following parameters determine the nature of the crawl.

  * MAX\_ROUNDS =  Maximum number of crawl rounds to performed.
  * MAX\_CRAWLED\_URLS = Max number of urls to be visited.
  * MAX\_PER\_URL =  Max number of related videos to be selected  from each url.
  * MAX\_PER\_PAGE = Max number of related videos to be considered for selection from each page
  * EXTRA\_NAME\_SERVERS = A list containing the name of the resolver and its IP address. This resolver will be used to get the IP address of the youtube cache.
  * PING\_PACKETS = Nb, of ping packets to be sent.
  * DOWNLOAD\_TIME = The duration for which the video must be downloaded.
  * BUFFERING\_VIDEO\_DURATION = The duration for which the video is to be buffered.
  * MIN\_PLAYOUT\_BUFFER\_SIZE = The size of the buffer for the video stream.
  * RESULT\_DIR = The directory to store the text results.
  * RESULT\_FILE = The file to store the text results.
  * DATABASE\_DIR = The directory to store the result database.
  * DATABASE = The name of the result database
  * TABLE = The name of the result table.
  * LOG\_DIR = The directory to store the log files.
  * LOG\_FILE = The file to store the logs.
  * LOG\_LEVEL = Parameter to set the log level(choose from DEBUG, INFO, WARNING, ERROR and CRITICAL)
  * PROXIES = The HTTP Proxy to be used.(Set from command-line at run-time by  user)

### lib\_youtube\_download.py ###

Module to download youtube video for a limited amount of time and calculate the different statistics needed for the analysis. It has the FileDownloader class and the YoutubeInfoExtractor class. The following functions defined in this module are used to get the statistics of the download.

**Usage**
> Terminal:
```
        python lib_youtube_download.py url
```
**Functions**
  * **get\_youtube\_cache\_url(url):**
> > Return the cache url of the youtube video.

  * **get\_download\_stats(ip\_address\_uri, downloadtime=config\_pytomo.DOWNLOADTIME):**
> > Returns a tuple of stats for download from an url based on ip
> > address. The tuple contains stats containing: `[`downloadtime,
> > data duration, datalength, video encodingrate, size of video in  bytes, Nb.of interruptions, accumulated buffer size, accumulated playback , current remaining buffer, Maximum Instant Throughput achieved `]`

### lib\_dns.py ###

Module to retrieve the IP address of a URL out of a set of nameservers (default nameservers and the ones provided in the config\_pytomo.py file as EXTRA\_NAME\_SERVERS).

**Usage**

> Not meant to be called directly. But provides the two functions
> discussed below.

**Functions**

  * **get\_default\_nameservers():**
> > Returns a list of IP addresses of default name servers.

  * **get\_ip\_addresses(url):**
> > Resolves the IP address of the url and returns a list of tuples with the IP address and the DNS resolver used. Multiple nameservers are tried. The default nameservers used are Google DNS, Open DNS, the default nameserver for the machine.

### lib\_ping.py ###

Module to generate the RTT times of a ping.This module has been configured to work on Linux, Windows and Mac systems.

**Usage**

> Not meant to be called directly. But provides the two functions
> discussed below.

**Functions**
  * **configure\_ping\_options(ping\_packets = config\_pytomo.PING\_PACKETS ):**
> > Function that generate the Regular Expression to match the RTT  patterns on different operating systems.
  * **ping\_ip(ipaddress, `[`pingpackets=config\_pytomo.PING\_PACKETS`]`):**
> > Returns a list of the min, avg and max ping values. Currently
> > designed to work with Windows, Mac and Linux systems.

### lib\_cache\_url.py ###

Module to retrieve the related videos from a file with a list of
Youtube links and to store it for next round of the crawl.

**Usage**

> Terminal:
> > lib\_cache\_url.py `[`-w out\_file`]` `[`-p 10`]` `[`-u 2`]` `[`-V`]` url\_file\_in


> Interactive python:
```
         import lib_cache_url
         urlfilein = 'urlfile.txt'
         lib_cache_url.get_next_round_urls(url_file_in, [max_per_page=20, max_per_url=5])
```
**Arguments**
  * **url\_file\_in:**File with a list of URLs to crawl (only Youtube is implemented).
  * **max\_per\_page:**Number of links to consider per page(only the first max\_per\_page related video links will be considered).
  * **max\_per\_url:** Number of links to select per page (max\_per\_url links will be randomly selected out of the max\_per\_page considered).

**Functions**
  * **get\_all\_links(url):**
> > Returns a list of all links from the url.
  * **get\_youtube\_links(url, max\_per\_page):**
> > Returns a set of links that direct to Youtube.
  * **trunk\_url(url):**
> > Returns the interesting part of a Youtube url(the url with
> > only the video ID).
  * **get\_related\_urls(url, `[`max\_per\_page=20, max\_per\_url=5`]`):**
> > Return a set of max\_per\_url links from max\_per\_page randomly
> > chosen related urls (other links are ignored).
  * **get\_next\_round\_urls(input\_links, max\_per\_page=20, max\_per\_url=5):**
> > Return a tuple of the set of input urls and a set of related url of videos.

### lib\_youtube\_api.py ###

Function to get the most popular Youtube videos according to the time frame.

**Usage**

> Not meant to be called directly. But provides one function as discussed below.

**Arguments**
  * **time**= 'today' or 'month' or 'week' or 'alltime'
  * **max\_results**= Total top videos needed (in  multiples of 25)

**Function**
  * **get\_popular\_links(time='today', `[`max\_results=25`]`):**
> > Returns the most popular Youtube links(world-wide). The number  of videos needed is given as max\_results. (The results returned are in no particular order).

### lib\_database.py ###

Module that creates and manages the database for th Pytomo results. It has PytomoDatabase class.The columns of the database are listed in the docstring of the module.

**Usage**

> Not meant to be called directly but the PytomoDatabase class is to be used.

**Functions**
The PytomoDatabase class has the following functions:

  * **create\_pytomo\_table(self, table=config\_pytomo.TABLE\_TIMESTAMP):**
> > Function to create a table.

  * **insert\_record(self, row):**
> > Function to insert a record into the database.

  * **fetch\_all(self):**
> > Function to print all the records of the table.

  * **close\_handle(self)**
> > Closes the connection to the database.

## kaa\_metadata ##

This is a stripped down version of the Kaa Metadata Python Package (Version :'0.7.7').The package has been modified to be used with the
lib\_youtube\_download.py module so that we can obtain the metadata of the video.The main modification was to make it independent of kaabase.

## dns ##

This is the DNS Python Package(Version : 1.9.2) that is used to obtain the nameservers for the machine and also to send DNS queries to the nameservers to obtain the IP addresses of the Youtube cache servers.

## logs/ ##

This folder contains the log files generated by the logger. These files contain the log details generated during the crawl run.

## databases/ ##

This folder contains the database files used to store the results.
The columns of the database are as follows:

  * Timestamp   -  A timestamp indicating the time of inserting the row.
  * Service     - The website on which the analysis is performed.Example: Youtube, Megavideo.
  * Url         - The url of the webpage.
  * CacheUrl   - The Url of the cache server hosting the video.
  * IP          - The IP address of the cache server from which the video is downloaded.
  * Resolver    - The DNS resolver used to get obtain the IP address of the cache server.Example Google DNS, Local DNS
  * DownloadTime  - The Time taken to download the video sample (We do not download the entire video but only for a limited download time.)
  * VideoType     - The format of the video that was downloaded.
  * VideoDuration - The actual duration of the complete video.
  * VideoLength   - The length(in bytes) of the complete video.
  * EncodingRate  - The encoding rate of the video.
  * DownloadBytes - The length of the video sample(in bytes).
  * DownloadInterruptions -  Nb of interruptions experienced during the download.
  * BufferingDuration -  Accumulate time spend in buffering state
  * PlaybackDuration - Accumulate time spend in playing state.
  * BufferDurationAtEnd     - The buffer length at the end of download.
  * PingMin     - The minimum recorded ping time to the resolved IP address of the cache server.
  * PingAvg     - The average recorded ping time to the resolved IP address of the cache server.
  * PingMax     - The maximum recorded ping time to the resolved IP address of the cache server.
  * RedirectUrl - In case of HTTP redirect while downloading the video from the cache server. The address of the URL to which the the request has been redirected is stored in this field.

## results/ ##

This folder contains the result files. The results in these file are listed in text format. It is a list containing `[Video url, Cache url, IP address of cache server, Ping RTT times to the Cache server, Download stats, Name - IP address of the DNS resolver]` where Download stats = `[`downloadtime, data duration, data length, video encoding rate, size of video in bytes, Nb.of interruptions, accumulated buffer-size, accumulated playback , current remaining buffer `]`


## External Links ##

  1. [Youtube Download.](http://rg3.github.com/youtube-dl/)
  1. [Kaa Metadata Python   Package.](http://packages.debian.org/sid/python-kaa-metadata)
  1. [DNS Python Package.](http://pypi.python.org/pypi/dnspython)