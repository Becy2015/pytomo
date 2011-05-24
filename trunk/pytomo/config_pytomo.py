#!/usr/bin/env python2.5
"""The config file for the pytomo setup
Lines starting with # are comments
"""

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# use package directory for storing files
# put it False if you want files in the current working dir (from where pytomo
# is launched)
USE_PACKAGE_DIR = False

RESULT_DIR = 'results'
RESULT_FILE = None
#RESULT_FILE = 'pytomo.result'

DATABASE_DIR = 'databases'
DATABASE = 'pytomo_database.db'
# DO NOT USE ANY . OR - IN THE TABLE NAME
TABLE = 'pytomo_crawl'

LOG_DIR = 'logs'
# log file use '-' for standard output
LOG_FILE = 'pytomo.log'
#LOG_FILE = '-'

# log level
# choose from: DEBUG, INFO, WARNING, ERROR and CRITICAL
LOG_LEVEL = DEBUG

# log the public IP address
LOG_PUBLIC_IP = True

# Image file to save the graphs
PLOT = False
 # List containig the column names to be plotted
COLUMN_NAMES = ['DownloadBytes', 'MaxInstantThp']
# Choose from  [ PingMin , PingAvg , PingMax , DownloadTime, VideoDuration
# VideoLength, EncodingRate, DownloadBytes, DownloadInterruptions,
# BufferingDuration, PlaybackDuration, BufferDurationAtEnd, MaxInstantThp]


IMAGE_FILE = 'pytomo_image.png'
IMAGE_DIR = 'plots'

################################################################################
# for start_pytomo.py

# TODO Static urls: to crawl each round
#STATIC_URL_FILE = ''

# Max number of rounds to perform
MAX_ROUNDS = 100
# Max number of urls to visit
MAX_CRAWLED_URLS = 50000
# Max number of related videos from each url
MAX_PER_URL = 2
# Max number of related videos from each page
MAX_PER_PAGE = 20

# timeframe for the most popular videos fetch at start of crawl
# put 'today', 'week', 'month' or 'all_time' (default case)
TIME_FRAME = 'week'

#Time delay between consecutive url crawls and download requests (in seconds)
DELAY_BETWEEN_REQUESTS = 10
# Max duration of round for getting input links
MAX_ROUND_DURATION = 600

IPADDR_TIMEOUT = 5

################################################################################
# for lib_cache_url.py
# proxy to set at command line
PROXIES = None
# replace with your values
#PROXIES = {'http': 'http://www.example.com:3128/'}

################################################################################
# for lib_dns.py

# other DNS servers to query
GOOGLE_PUBLIC_DNS = ('google_public_dns', '8.8.8.8')
OPEN_DNS = ('open_dns', '208.67.220.220')
# The lifetime of a DNS query(in seconds). The default is 30 seconds.
DNS_TIMEOUT = 4.0
EXTRA_NAME_SERVERS = [GOOGLE_PUBLIC_DNS, OPEN_DNS]
EXTRA_NAME_SERVERS_CC = []

# HTTP codes to check for redirects.
HTTP_REDIRECT_CODE = 301
HTTP_OK = 200
MAX_NB_REDIRECT = 8

################################################################################
# for lib_ping.py
# nb of packets to send for ping stats
PING_PACKETS = 3

################################################################################
# for lib_youtube_download.py
DOWNLOAD_TIME = 8.0
BUFFERING_VIDEO_DURATION = 3.0
MIN_PLAYOUT_BUFFER_SIZE = 1.0

# nb of tries for extracting metadata info from video
MAX_NB_TRIES_ENCODING = 9
################################################################################
################################################################################
# to be set by start_pytomo.py: DO NOT CHANGE
LOG = None
LOG_FILE_TIMESTAMP = None
DATABASE_TIMESTAMP = None
TABLE_TIMESTAMP = None
SYSTEM = None
RTT = None

SEP_LINE = 80 * '#'
NB_IDENT_VALUES = 5
NB_PING_VALUES = 3
NB_DOWNLOAD_VALUES = 11
NB_REDIRECT_VALUES = 1
NB_FIELDS = (NB_IDENT_VALUES + NB_PING_VALUES + NB_DOWNLOAD_VALUES
             + NB_REDIRECT_VALUES)

USER_INPUT_TIMEOUT = 5

LEVEL_TO_NAME = {DEBUG: 'DEBUG',
                 INFO: 'INFO',
                 WARNING: 'WARNING',
                 ERROR: 'ERROR',
                 CRITICAL: 'CRITICAL'}

NAME_TO_LEVEL = {'DEBUG': DEBUG,
                 'INFO': INFO,
                 'WARNING': WARNING,
                 'ERROR': ERROR,
                 'CRITICAL': CRITICAL}

################################################################################
# black list utils

BLACK_LISTED = 'das_captcha'

class BlackListException(Exception):
    "Exception in case the crawler has been blacklisted"
    pass

