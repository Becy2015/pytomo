#!/usr/bin/env python
"""
Module to launch a crawl.
This module supplies the following functions that can be used
independently:
    1. compute_stats: To calculate the download statistics of a URL.

   Usage:
       To use the functions provided in this module independently,
   first place yourself just above pytomo folder.Then:

   import pytomo.start_pytomo as start_pytomo
   import config_pytomo as config_pytomo
   import platform
   config_pytomo.SYSTEM = platform.system()
   url = 'http://www.youtube.com/watch?v=cv5bF2FJQBc'
   start_pytomo.compute_stats(url)
"""

from __future__ import with_statement, absolute_import

import sys
from urlparse import urlsplit
from pprint import pprint
import logging
import datetime
from time import strftime, timezone
import os
from string import maketrans
from optparse import OptionParser
import hashlib
import socket
import urllib2
import platform
import signal
import time
from os.path import abspath, dirname, sep
from sys import path
import tarfile

# assumes the standard distribution paths
PACKAGE_DIR = dirname(abspath(path[0]))

PUBLIC_IP_FINDER = 'http://automation.whatismyip.com/n09230945.asp'

SEPARATOR_LINE = '#' * 80

try:
    from win32com.shell import shell, shellcon
    HOME_DIR = shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)
except ImportError:
    HOME_DIR = os.path.expanduser('~')

from . import config_pytomo
from . import lib_cache_url
from . import lib_dns
from . import lib_ping
from . import lib_youtube_download
from . import lib_database
from . import lib_youtube_api

if config_pytomo.PLOT:
    from . import lib_plot

# only 1 service is implemented
SERVICE = 'Youtube'

def compute_stats(url):
    "Return a list of the statistics related to the url"
    cache_uri = lib_youtube_download.get_youtube_cache_url(url)
    if not cache_uri:
        # no cache uri found => skip crawl
        return None
    current_stats = dict()
    # <scheme>://<netloc>/<path>?<query>#<fragment>
    parsed_uri = urlsplit(cache_uri)
    cache_url = '://'.join((parsed_uri.scheme, parsed_uri.netloc))
    cache_urn = '?'.join((parsed_uri.path, parsed_uri.query))
    ip_addresses = lib_dns.get_ip_addresses(parsed_uri.netloc)
    for (ip_address, resolver) in ip_addresses:
        config_pytomo.LOG.debug("Compute stats for IP: %s" % ip_address)
        timestamp = datetime.datetime.now()
        if ip_address in current_stats:
            # if stats already computed, just indicate a new resolver in the
            # result list
            current_stats[ip_address][-1] = ('%s_%s' %
                                             (current_stats[ip_address][-1],
                                              resolver))
            config_pytomo.LOG.debug("Skip IP already crawled: %s"
                                    % ip_address)
            continue
        ping_times = lib_ping.ping_ip(ip_address)
        # it's important to pass the uri with the ip_address to avoid
        # uncontrolled DNS resolution
        ip_address_uri = ('://'.join((parsed_uri.scheme, ip_address)) +
                          cache_urn)
        status_code, download_stats, redirect_url = (
                lib_youtube_download.get_download_stats(ip_address_uri))
        current_stats[ip_address] = [timestamp, ping_times, download_stats,
                                     redirect_url, resolver]
    # TODO: check if cache_url is the same independently of DNS
    return status_code, (url, cache_url, current_stats)

def format_stats(stats):
    """Return the stats as a list of tuple to insert into database
    Doctest:

    >>> stats = ('http://www.youtube.com/watch?v=RcmKbTR--iA',
    ...            'http://v15.lscache3.c.youtube.com',
    ...             {'173.194.20.56': [datetime.datetime(
    ...                                 2011, 5, 6, 15, 30, 50, 103775),
    ...                                 None,
    ...                                [8.9944229125976562, 'mp4',
    ...                                225,
    ...                                115012833.0,
    ...                                511168.14666666667,
    ...                                9575411,
    ...                                0,
    ...                                0.99954795837402344,
    ...                                7.9875903129577637,
    ...                                11.722306421319782,
    ...                                1192528.8804511931],
    ...                              'default_10.193.225.12', None]})

    >>> format_stats(stats) #doctest: +NORMALIZE_WHITESPACE
        [(datetime.datetime(2011, 5, 6, 15, 30, 50, 103775),
          'Youtube', 'http://www.youtube.com/watch?v=RcmKbTR--iA',
      'http://v15.lscache3.c.youtube.com', '173.194.20.56',
      None, None, None, None, 8.9944229125976562,
      'mp4', 225, 115012833.0, 511168.14666666667, 9575411, 0,
     0.99954795837402344, 7.9875903129577637, 11.722306421319782,
      1192528.8804511931, 'default_10.193.225.12')]

    >>> stats = ('http://www.youtube.com/watch?v=OdF-oiaICZI',
    ...  'http://v7.lscache8.c.youtube.com',
    ...                 {'74.125.105.226': [datetime.datetime(
    ...                                       2011, 5, 6, 15, 30, 50, 103775),
    ...                                     [26.0, 196.0, 82.0],
    ...                                     [30.311000108718872, 'mp4',
    ...                                      287.487, 16840065.0,
    ...                                      58576.78781997099,
    ...                                      1967199, 0,
    ...                                      1.316999912261963,
    ...                                      28.986000061035156,
    ...                                      5.542251416248594,
    ...                                      1109.4598961624772],
    ...                   'google_public_dns_8.8.8.8_open_dns_208.67.220.220',
    ...                                 'http://www.youtube.com/fake_redirect'],
    ...                  '173.194.8.226': [datetime.datetime(2011, 5, 6, 15,
    ...                                                       30, 51, 103775),
    ...                                    [103.0, 108.0, 105.0],
    ...                                    [30.287999868392944, 'mp4',
    ...                                     287.487, 16840065.0,
    ...                                     58576.78781997099,
    ...                                     2307716,
    ...                                     0,
    ...                                     1.3849999904632568,
    ...                                     28.89300012588501,
    ...                                     11.47842453761781,
    ...                                     32770.37517215069],
    ...                                    'default_212.234.161.118', None]})


    >>> format_stats(stats) #doctest: +NORMALIZE_WHITESPACE
    [(datetime.datetime(2011, 5, 6, 15, 30, 50, 103775),
       'Youtube', 'http://www.youtube.com/watch?v=OdF-oiaICZI',
      'http://v7.lscache8.c.youtube.com', '74.125.105.226',
      'http://www.youtube.com/fake_redirect', 26.0, 196.0, 82.0,
      30.311000108718872, 'mp4', 287.48700000000002, 16840065.0,
      58576.787819970988, 1967199, 0, 1.3169999122619629,
      28.986000061035156, 5.5422514162485941, 1109.4598961624772,
      'google_public_dns_8.8.8.8_open_dns_208.67.220.220'),
     (datetime.datetime(2011, 5, 6, 15, 30, 51, 103775),
       'Youtube', 'http://www.youtube.com/watch?v=OdF-oiaICZI',
      'http://v7.lscache8.c.youtube.com', '173.194.8.226',
      None, 103.0, 108.0, 105.0, 30.287999868392944,
      'mp4', 287.48700000000002, 16840065.0, 58576.787819970988, 2307716,
      0, 1.3849999904632568, 28.89300012588501, 11.47842453761781,
      32770.375172150692, 'default_212.234.161.118')]
"""
    record_list = []
    (url, cache_url, current_stats) = stats
    for (ip_address, values) in current_stats.items():
        (timestamp, ping_times, download_stats, redirect_url, resolver) = values
        if not ping_times:
            ping_times = [None] * config_pytomo.NB_PING_VALUES
        if not download_stats:
            download_stats = [None] * config_pytomo.NB_DOWNLOAD_VALUES
        # use inet_aton(ip_address) for optimisation on this field
        row = ([timestamp, SERVICE, url, cache_url, ip_address, resolver]
               + list(ping_times) + download_stats + [redirect_url])
        record_list.append(tuple(row))
    return record_list

def check_out_files(file_pattern, directory, timestamp):
    """Return a full path of the file used for the output
    Test if the path exists, create if possible or create it in default user
    directory

    >>> file_pattern = None
    >>> directory = 'logs'
    >>> timestamp = 'doc_test'
    >>> check_out_files(file_pattern, directory, timestamp) #doctest: +ELLIPSIS
    >>> file_pattern = 'pytomo.log'
    >>> check_out_files(file_pattern, directory, timestamp) #doctest: +ELLIPSIS
    '...doc_test.pytomo.log'

    """
    if file_pattern == None:
        return None
    if config_pytomo.USE_PACKAGE_DIR:
        base_dir = PACKAGE_DIR
    else:
        base_dir = os.getcwd()
    if directory:
        out_dir = sep.join((base_dir, directory))
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir)
            except OSError, mes:
                config_pytomo.LOG.warn(
                    'Out dir %s does not exist and cannot be created\n%s'
                    % (out_dir, mes))
                if HOME_DIR:
                    config_pytomo.LOG.warn('Will use home base dir: %s'
                                           % HOME_DIR)
                    out_dir = sep.join((HOME_DIR, directory))
                    if not os.path.exists(out_dir):
                        # do not catch OSError as it's our second attempt
                        os.makedirs(out_dir)
                else:
                    config_pytomo.LOG.error(
                        'Impossible to create output file: %s' % file_pattern)
                    raise IOError
    else:
        out_dir = os.getcwd()
    out_file = sep.join((out_dir, '.'.join((socket.gethostname(), timestamp,
                                            file_pattern))))
    # do not catch IOError
    with open(out_file, 'a') as _:
        # just test writing in the out file
        pass
    return out_file

def md5sum(input_file):
    "Return the standard md5 of the file"
    # to cope with large files
    # value taken from Python distribution
    try:
        input_stream = open(input_file, 'rb')
    except (TypeError, IOError), mes:
        config_pytomo.LOG.exception('Unable to compute the md5 of file: %s'
                                    % mes)
        return None
    bufsize = 8096
    hash_value = hashlib.md5()
    while True:
        data = input_stream.read(bufsize)
        if not data:
            break
        hash_value.update(data)
    return hash_value.hexdigest()

class MaxUrlException(Exception):
    "Class to stop crawling when the max nb of urls has been attained"
    pass

def crawl_links(input_links, crawled_urls, result_stream=None, data_base=None):
    "Crawl each input link"
    max_crawled_urls = config_pytomo.MAX_CRAWLED_URLS
    max_per_page = config_pytomo.MAX_PER_PAGE
    max_per_url = config_pytomo.MAX_PER_URL
    next_urls = set()
    for url in input_links:
        config_pytomo.LOG.info("Crawl of url # %d" % len(crawled_urls))
        config_pytomo.LOG.debug("Crawl url: %s" % url)
        if url in crawled_urls:
            config_pytomo.LOG.debug("Skipped url already crawled: %s"
                                    % url)
            continue
        if len(crawled_urls) >= max_crawled_urls:
            raise MaxUrlException()
        if result_stream:
            print >> result_stream, config_pytomo.SEP_LINE
        status_code, nb_redirects = None, 0
        stats = None
        while (nb_redirects <= config_pytomo.MAX_NB_REDIRECT
               and (status_code == config_pytomo.HTTP_REDIRECT_CODE
                    or not status_code)):
            try:
                status_code, stats = compute_stats(url)
            except TypeError:
                config_pytomo.LOG.error('Error retrieving stats for : %s' %url)
                break
            if status_code == config_pytomo.HTTP_REDIRECT_CODE:
                nb_redirects += 1
            if stats:
                crawled_urls.add(url)
                if result_stream:
                    pprint(stats, stream=result_stream)
                if data_base:
                    for row in format_stats(stats):
                        data_base.insert_record(row)
                else:
                    config_pytomo.LOG.info('no stats for url: %s' % url)
                # wait only if there were stats retrieved
                time.sleep(config_pytomo.DELAY_BETWEEN_REQUESTS)
        if len(next_urls) < config_pytomo.MAX_CRAWLED_URLS:
            related_urls = set(filter(None, lib_cache_url.get_related_urls(url,
                                                   max_per_page, max_per_url)))
            next_urls = next_urls.union(related_urls)
    return next_urls.difference(input_links)

def do_crawl(result_stream=None, db_file=None, timestamp=None, image_file=None):
    """Crawls the urls given by the url_file
    up to max_rounds are performed or max_visited_urls
    """
    if not db_file and not result_stream:
        config_pytomo.LOG.critical('Cannot start crawl because no file can '
                                   'store output')
        return
    config_pytomo.LOG.critical('Start crawl')
    if not timestamp:
        timestamp = strftime("%Y-%m-%d.%H_%M_%S")
    data_base = None
    if db_file:
        config_pytomo.DATABASE_TIMESTAMP = db_file
        trans_table = maketrans('.-', '__')
        config_pytomo.TABLE_TIMESTAMP = '_'.join((config_pytomo.TABLE,
                                              timestamp)).translate(trans_table)
        data_base = lib_database.PytomoDatabase(
                                            config_pytomo.DATABASE_TIMESTAMP)
        data_base.create_pytomo_table(config_pytomo.TABLE_TIMESTAMP)
    max_rounds = config_pytomo.MAX_ROUNDS
#    max_per_page = config_pytomo.MAX_PER_PAGE
#    max_per_url = config_pytomo.MAX_PER_URL
    input_links = set(filter(None,
                             lib_youtube_api.get_popular_links(
                                 time=config_pytomo.TIME_FRAME,
                                 max_results=config_pytomo.MAX_PER_PAGE)))
    crawled_urls = set()
    for round_nb in xrange(max_rounds):
        config_pytomo.LOG.warn("Round %d started\n%s"
                               % (round_nb, config_pytomo.SEP_LINE))
        # Reseting the name servers at start of each crawl
        config_pytomo.EXTRA_NAME_SERVERS_CC = (
                                config_pytomo.EXTRA_NAME_SERVERS[:])
        config_pytomo.LOG.info("Name servers at round %s:"
                               % config_pytomo.EXTRA_NAME_SERVERS_CC)
        try:
            input_links = crawl_links(input_links, crawled_urls, result_stream,
                                      data_base)
        except MaxUrlException:
            config_pytomo.LOG.warn("Stopping crawl because already crawled "
                                   "%d urls" % len(crawled_urls))
            break
        time.sleep(config_pytomo.DELAY_BETWEEN_REQUESTS)
        # The plot is redrawn everytime the database is updated
        if config_pytomo.PLOT:
            lib_plot.plot_data(db_file, config_pytomo.COLUMN_NAMES,
                               image_file)
        # next round input are related links of the current input_links
#        input_links = lib_cache_url.get_next_round_urls(input_links,
#                                                        max_per_page,
#                                                        max_per_url)
    if data_base:
        data_base.close_handle()
    config_pytomo.LOG.warn("Crawl finished\n" + config_pytomo.SEP_LINE)

def convert_debug_level(_, __, value, parser):
    "Convert the string passed to a logging level"
    try:
        log_level = config_pytomo.NAME_TO_LEVEL[value.upper()]
    except KeyError:
        parser.error("Incorrect log level.\n"
                     "Choose from: 'DEBUG', 'INFO', 'WARNING', "
                     "'ERROR' and 'CRITICAL' (default '%s')"
                     % config_pytomo.LEVEL_TO_NAME[
                         config_pytomo.LOG_LEVEL])
        return
    setattr(parser.values, 'LOG_LEVEL', log_level)

def set_proxies(_, __, value, parser):
    "Convert the proxy passed to a dict to be handled by urllib2"
    if value:
        # remove quotes
        value = value.translate(None, '\'"')
        if not value.startswith('http://'):
            value = 'http://'.join(('', value))
        setattr(parser.values, 'PROXIES', {'http': value})

def create_options(parser):
    "Add the different options to the parser"
    parser.add_option("-r", dest="MAX_ROUNDS", type='int',
                      help=("Max number of rounds to perform (default %d)"
                            % config_pytomo.MAX_ROUNDS),
                      default=config_pytomo.MAX_ROUNDS)
    parser.add_option("-u", dest="MAX_CRAWLED_URL", type='int',
                      help=("Max number of urls to visit (default %d)"
                            % config_pytomo.MAX_CRAWLED_URLS),
                      default=config_pytomo.MAX_CRAWLED_URLS)
    parser.add_option("-p", dest="MAX_PER_URL", type='int',
                      help=("Max number of related urls from each page "
                            "(default %d)" % config_pytomo.MAX_PER_URL),
                      default=config_pytomo.MAX_PER_URL)
    parser.add_option("-P", dest="MAX_PER_PAGE", type='int',
                      help=("Max number of related videos from each page "
                            "(default %d)" % config_pytomo.MAX_PER_PAGE),
                      default=config_pytomo.MAX_PER_PAGE)
    parser.add_option("-t", dest="TIME_FRAME", type='string',
                      help=("Timeframe for the most popular videos to fetch "
                            "at start of crawl put 'today', 'week', 'month' "
                            "or 'all_time' (default '%s')"
                            % config_pytomo.TIME_FRAME),
                      default=config_pytomo.TIME_FRAME)
    parser.add_option("-n", dest="PING_PACKETS", type='int',
                      help=("Number of packets to be sent for each ping "
                            "(default %d)" % config_pytomo.PING_PACKETS),
                      default=config_pytomo.PING_PACKETS)
    parser.add_option("-D", dest="DOWNLOAD_TIME", type='float',
                      help=("Download time for the video in seconds (default %f)"
                            % config_pytomo.DOWNLOAD_TIME),
                      default=config_pytomo.DOWNLOAD_TIME)
    parser.add_option("-B", dest="INITIAL_PLAYBACK_DURATION ", type='float',
                      help=("Buffering video duration in seconds (default %f)"
                            % config_pytomo.INITIAL_PLAYBACK_DURATION),
                      default=config_pytomo.INITIAL_PLAYBACK_DURATION )
    parser.add_option("-M", dest="MIN_PLAYOUT_BUFFER_SIZE", type='float',
                      help=("Minimum Playout Buffer Size in seconds (default %f)"
                            % config_pytomo.MIN_PLAYOUT_BUFFER),
                      default=config_pytomo.MIN_PLAYOUT_BUFFER)
    parser.add_option("-x", dest="LOG_PUBLIC_IP", action="store_false",
                      help=("Do NOT store public IP address of the machine "
                            "in the logs"), default=config_pytomo.LOG_PUBLIC_IP)
    parser.add_option("-L", dest="LOG_LEVEL", type='string',
                      help=("The log level setting for the Logging module."
                            "Choose from: 'DEBUG', 'INFO', 'WARNING', "
                            "'ERROR' and 'CRITICAL' (default '%s')"
                            % config_pytomo.LEVEL_TO_NAME[
                                config_pytomo.LOG_LEVEL]),
                      default=config_pytomo.LOG_LEVEL, action='callback',
                      callback=convert_debug_level)
    parser.add_option("--http-proxy", dest="PROXIES", type='string',
                      help=("in case of http proxy to reach Internet "
                            "(default %s)" % config_pytomo.PROXIES),
                      default=config_pytomo.PROXIES, action='callback',
                     callback=set_proxies)

def check_options(parser, options):
    "Check incompatible options"
    if options.TIME_FRAME not in (['today', 'week', 'month', 'all_time']):
        parser.error("Incorrect time frame.\n"
                     "Choose from: 'today', 'week', 'month', 'all_time' "
                     "(default '%s')" % config_pytomo.TIME_FRAME)

def write_options_to_config(options):
    "Write read options to config_pytomo"
    for name, value in options.__dict__.items():
        setattr(config_pytomo, name, value)

def log_ip_address():
    "Log the remote IP addresses"
    print ("Logging the local public IP address.")
    # is local address of some interest??
    # check: http://stackoverflow.com/
    # questions/166506/finding-local-ip-addresses-in-python
    if config_pytomo.PROXIES:
        proxy = urllib2.ProxyHandler(config_pytomo.PROXIES)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
    try:
        if sys.hexversion >= int(0x2060000):
            # timeout is available only python above 2.6
            public_ip = urllib2.urlopen(PUBLIC_IP_FINDER, None,
                                        config_pytomo.IPADDR_TIMEOUT).read()
        else:
            public_ip = urllib2.urlopen(PUBLIC_IP_FINDER, None).read()
    except urllib2.URLError, mes:
        config_pytomo.LOG.critical('Public IP address not found: %s' % mes)
        print 'Public IP address not found: %s' % mes
        public_ip = None
    else:
        config_pytomo.LOG.critical('Machine has this public IP address: %s'
                                   % public_ip)
        print 'Machine has this public IP address: %s' % public_ip

def log_md5_results(result_file, db_file):
    "Computes and stores the md5 hash of result and database files"
    if db_file:
        config_pytomo.LOG.critical('Hash of database file: %s'
                                   % md5sum(db_file))
    if result_file and result_file != sys.stdout:
        config_pytomo.LOG.critical('Hash of result file: %s'
                                   % md5sum(result_file))

def configure_log_file(timestamp):
    "Configure log file and indicate succes or failure"
    print "Configuring log file"
    # to have kaa-metadata logs
    config_pytomo.LOG = logging.getLogger('metadata')
    if config_pytomo.LOG_FILE == '-':
        handler = logging.StreamHandler(sys.stdout)
        print "Logs are on standard output"
    else:
        try:
            log_file = check_out_files(config_pytomo.LOG_FILE,
                                       config_pytomo.LOG_DIR, timestamp)
        except IOError:
            print >> sys.stderr, ("Problem opening file with timestamp: %s"
                                  % timestamp)
            return None
        print "Logs are there: %s" % log_file
        # for lib_youtube_download
        config_pytomo.LOG_FILE_TIMESTAMP = log_file
        handler = logging.FileHandler(filename=log_file)
    log_formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - "
                                      "%(levelname)s - %(message)s")
    handler.setFormatter(log_formatter)
    config_pytomo.LOG.addHandler(handler)
    config_pytomo.LOG.setLevel(config_pytomo.LOG_LEVEL)
    config_pytomo.LOG.critical('Log level set to %s',
                           config_pytomo.LEVEL_TO_NAME[config_pytomo.LOG_LEVEL])
    # to not have console output
    config_pytomo.LOG.propagate = False
    # log all config file values except built in values
    for value in filter(lambda x: not x.startswith('__'),
                        config_pytomo.__dict__):
        config_pytomo.LOG.critical('%s: %s'
                                   % (value, getattr(config_pytomo, value)))
    return log_file

class MyTimeoutException(Exception):
    "Class to generate timeout exceptions"
    pass

def log_provider(timeout=config_pytomo.USER_INPUT_TIMEOUT):
    "Get and logs the provider from the user or skip after timeout seconds"
    def timeout_handler(signum, frame):
        "handle the timeout"
        raise MyTimeoutException()
    # non-posix support for signals is weak
    support_signal = hasattr(signal, 'SIGALRM') and hasattr(signal, 'alarm')
    if support_signal:
        signal.signal(signal.SIGALRM, timeout_handler)
        # triger alarm in timeout seconds
        signal.alarm(timeout)
    try:
        provider = prompt_provider(support_signal, timeout)
    except MyTimeoutException:
        return None
    finally:
        if support_signal:
            # alarm disabled
            signal.alarm(0)
    config_pytomo.LOG.critical('User has given this provider: %s' % provider)
    return provider

def prompt_provider(support_signal, timeout):
    "Function to prompt for provider"
    return raw_input(''.join((
            "Please indicate your provider/ISP (leave blank for skipping).\n",
            "Crawl will START when you PRESS ENTER",
            ((" (or after %d seconds)" % timeout) if support_signal else ''),
            ".\n")))


def prompt_start_crawl():
    "Funtion to prompt user for to accept the crawling"
    return raw_input('Are you ok to start crawling? (Y/N)\n')

def main(version=None,argv=None):
    """Program wrapper
    Setup of log part
    """
    if not argv:
        argv = sys.argv[1:]
    usage = ("%prog [-r max_rounds] [-u max_crawled_url] [-p max_per_url] "
             "[-P max_per_page] [-t time_frame] [-n ping_packets] "
             "[-D download_time] [-B buffering_video_duration] "
             "[-M min_playout_buffer_size] [-x] [-L log_level]")
    parser = OptionParser(usage=usage)
    create_options(parser)
    (options, _) = parser.parse_args(argv)
    check_options(parser, options)
    write_options_to_config(options)
    timestamp = strftime("%Y-%m-%d.%H_%M_%S")
    log_file = configure_log_file(timestamp)
    image_file = None
    if not log_file:
        return -1
    try:
        result_file = check_out_files(config_pytomo.RESULT_FILE,
                                      config_pytomo.RESULT_DIR, timestamp)
    except IOError:
        result_file = None
    if result_file:
        print "Text results are there: %s" % result_file
    try:
        db_file = check_out_files(config_pytomo.DATABASE,
                                  config_pytomo.DATABASE_DIR, timestamp)
    except IOError:
        db_file = None
    if db_file:
        print "Database results are there: %s" % db_file
    config_pytomo.LOG.critical('Offset between local time and UTC: %d'
                               % timezone)
    config_pytomo.LOG.warn('Pytomo version = %s' % version)
    config_pytomo.SYSTEM = platform.system()
    config_pytomo.LOG.warn('Pytomo is running on this system: %s'
                           % config_pytomo.SYSTEM)
    if config_pytomo.LOG_PUBLIC_IP:
        log_ip_address()
    if config_pytomo.PLOT:
        try:
            image_file = check_out_files(config_pytomo.IMAGE_FILE,
                                    config_pytomo.IMAGE_DIR, timestamp)
        except IOError:
            image_file = None
        if image_file:
            print "Plots are here: %s" % image_file
        else:
            print "Unable to create image_file"
    while True:
        start_crawl = prompt_start_crawl()
        if start_crawl.upper() == 'N':
            return 0
        elif start_crawl.upper() == 'Y':
            break
    log_provider(timeout=config_pytomo.USER_INPUT_TIMEOUT)
    print "Type Ctrl-C to interrupt crawl"
    try:
        result_stream = None
        # memory monitoring module
        if result_file:
            result_stream = open(result_file, 'w')
        do_crawl(result_stream=result_stream, db_file=db_file,
                 image_file=image_file, timestamp=timestamp)
        if config_pytomo.PLOT:
            lib_plot.plot_data(db_file, config_pytomo.COLUMN_NAMES,
                               image_file)
        if result_file:
            result_stream.close()
    except config_pytomo.BlackListException:
        err_mes = ('Crawl detected by YouTube: '
                   'log to YouTube and enter captcha')
        config_pytomo.LOG.critical(err_mes)
        print err_mes
    except KeyboardInterrupt:
        config_pytomo.LOG.critical('Crawl interrupted by user')
    except Exception, mes:
        config_pytomo.LOG.exception('Uncaught exception: %s' % mes)
    log_md5_results(result_file, db_file)
    tarfile_name = check_out_files('to_send.tbz',
                                   config_pytomo.LOG_DIR, timestamp)
    tar_file = tarfile.open(name=tarfile_name, mode='w:bz2')
    tar_file.add(db_file, arcname=os.path.basename(db_file))
    tar_file.add(log_file, arcname=os.path.basename(log_file))
    tar_file.close()
    print ('\nCrawl finished.\n%s\n\nPLEASE SEND THIS FILE BY EMAIL: '
           '(to pytomo@gmail.com)\n%s\n'
           % (SEPARATOR_LINE, tarfile_name))
    raw_input('Press Enter to exit\n')
    return 0

if __name__ == '__main__':
    #sys.exit(main())
    import doctest
    doctest.testmod()
