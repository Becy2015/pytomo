#!/usr/bin/env python
"""
    Mock test module for the start_pytomo.py module
    pylint --ignored-classes=nose.tools test_start_pytomo.py

"""
from __future__ import absolute_import
import nose.tools as ntools

from ..pytomo import start_pytomo
from ..pytomo import lib_youtube_download
from ..pytomo import lib_youtube_api
from ..pytomo import lib_cache_url
from ..pytomo import config_pytomo
from ..pytomo import lib_dns
from ..pytomo import lib_ping
from ..pytomo import lib_database

import doctest
doctest.testmod(start_pytomo)

import sys
from StringIO import StringIO

# Mock test for start_pytomo.compute_stats
#http://stackoverflow.com/questions/2658026/how-to-change-the-date-time-in-
#python-for-all-modules
real_datetime = None

def patch_compute_stats():
    """Function to patch the namespace of the function used. Did not patch
    datetime.datetime as it an internal module implemented in C and patching it
    may have unepected side-effects on other modules."""
    from platform import system
    config_pytomo.SYSTEM = system()
    start_pytomo.configure_log_file('mock_test')
    "Module to patch the namespace of funtions used in compute_stats "
    cache_url = (
         ''.join(('http://v6.lscache3.c.youtube.com/videoplayback?',
                  't%2Cfactor&fexp=901316%2C907605%2C911600%2C910206',
                  '&algorithm=throttle-',
                  'factor&itag=34&ipbits=8&burst=40&sver=3&',
                  'signature=3245139EA994D3298F6124AED1502EB6D9C9047C.',
                  '90B3EE7150216E453FA83734DBA125E82E15DACC',
                  '&expire=1302883200&key=yt1&ip=193.0.0.0',
                  '&factor=1.25&id=72fe5b1761494017'
                 )))
    lib_youtube_download._get_youtube_cache_url = (
                    lib_youtube_download.get_youtube_cache_url)
    lib_youtube_download.get_youtube_cache_url = lambda x: cache_url
    lib_dns._get_ip_addresses = lib_dns.get_ip_addresses
    lib_dns.get_ip_addresses = lambda x: [('127.0.0.1', 'mock_resolver')]
    lib_ping._ping_ip =  lib_ping.ping_ip
    lib_ping.ping_ip = lambda x : ['00.00', '00.00', '00.00']
    lib_youtube_download._get_download_stats = (
                lib_youtube_download.get_download_stats)
    lib_youtube_download.get_download_stats = lambda x : (200, [],
                                                          'redirect_url')

def unpatch_compute_stats():
    "Function to clear the patch"
    lib_youtube_download.get_youtube_cache_url = (
                    lib_youtube_download._get_youtube_cache_url)
    delattr(lib_youtube_download, '_get_youtube_cache_url')
    lib_dns.get_ip_addresses = lib_dns._get_ip_addresses
    delattr(lib_dns, '_get_ip_addresses')
    lib_ping._ping_ip =  lib_ping.ping_ip
    delattr(lib_ping, '_ping_ip')
    datetime = real_datetime

@ntools.with_setup(patch_compute_stats, unpatch_compute_stats)
def test_compute_stats():
    "Test for compute_stats function"
    url = "http://www.youtube.com/watch?v=cv5bF2FJQBc"
    res = start_pytomo.compute_stats(url)
    ntools.assert_equals(res[0], 200)
    ntools.assert_equals(res[1][0],'http://www.youtube.com/watch?v=cv5bF2FJQBc')
    ntools.assert_equals(res[1][1], 'http://v6.lscache3.c.youtube.com')
    stats = res[1][2]['127.0.0.1'][1:]
    expected_stats = [['00.00', '00.00', '00.00'], [], 'mock_resolver',
                      'redirect_url']
    ntools.assert_equals(stats, expected_stats)

# Mock test for start_pytomo.check_out_files
def test_check_out_files():
    "Test for the check_out_files function"
    res = start_pytomo.check_out_files(None, 'mock_dir', 'mock_timestamp')
    ntools.assert_equals(res, None)
    res = start_pytomo.check_out_files('mock_test_file',
                                       'mock_dir', 'mock_time')
    ntools.assert_true(res.find('mock_time.mock_test_file'))
    ntools.assert_true(res.find('mock_dir'))

# Mock test for crawl_links
def patch_crawl_links():
    import datetime
    "Function to patch the namespace of the function used."
    start_pytomo._compute_stats = start_pytomo.compute_stats
    start_pytomo.configure_log_file('mock_test')
    compute_stats_res = (200,
                          ('http://www.youtube.com/watch?v=OdF-oiaICZI',
                             'http://v7.lscache8.c.youtube.com',
                           {'173.194.20.107': [
                            datetime.datetime(2011, 5, 19, 14, 3, 3, 307787),
                                               None,
                                               [9.5496759414672852,
                                                'flv',
                                                287.48700000000002,
                                                16840065.0,
                                                468614.30255976791,
                                                2708143,
                                                1,
                                                7.5402472019195557,
                                                1.9848883152008057,
                                                -0.86470310986144128,
                                                1006878.7800146521],
                                               'default_10.193.225.12',
                                               None]}))

    start_pytomo.compute_stats = lambda x : compute_stats_res
    start_pytomo._format_stats = start_pytomo.format_stats
    format_stats_res = [(datetime.datetime(2011, 5, 19, 14, 13, 21, 879017),
                           'Youtube',
                           'http://www.youtube.com/watch?v=OdF-oiaICZI',
                           'http://v7.lscache8.c.youtube.com',
                           '173.194.20.107',
                           'default_10.193.225.12',
                           None,
                           None,
                           None,
                           8.7971951961517334,
                           'flv',
                           287.48700000000002,
                           16840065.0,
                           468614.30255976791,
                           2653658,
                           1,
                           6.7759432792663574,
                           2.0163519382476807,
                           -0.14690575906265835,
                           197469.76073563218,
                           None)]
    start_pytomo.format_stats = lambda x: format_stats_res

# Mock test for crawl_links
def unpatch_crawl_links():
    "Function to clear the patch"
    start_pytomo.compute_stats = start_pytomo._compute_stats
    delattr(start_pytomo, '_compute_stats')
    start_pytomo.format_stats = start_pytomo._format_stats
    delattr(start_pytomo, '_format_stats')

@ntools.with_setup(patch_crawl_links, unpatch_crawl_links)
def test_crawl_links():
    "Function to test the crawl links function"
    input_links = ['http://www.youtube.com/watch?v=cv5bF2FJQBc']
    mock_file_name = 'mock_file'
    mock_file = open(mock_file_name, 'w+r')
    # Test for the case when the input link is new
    crawled_urls = set()
    data_base = lib_database.PytomoDatabase('mock_db.db')
    data_base.create_pytomo_table('mock_table')
#    start_pytomo.crawl_links(input_links, crawled_urls,
#                      mock_file, data_base)
#    with open(mock_file_name, 'r') as mock_file:
#        k = mock_file.readlines()
#        #Check if results are being stored
#        ntools.assert_false(len(k) == 0)
#    #Test for the case when link was already crawled
    crawled_urls = input_links
    mock_file = open(mock_file_name, 'w+r')
    start_pytomo.crawl_links(input_links, crawled_urls,
                      mock_file, None)
    with open(mock_file_name, 'r') as mock_file:
        k = mock_file.readlines()
       # None should be returned
    ntools.assert_false(k)

#Mock test for do_crawl

def raise_maxurlexception(*args):
    "Raise Exception MaxUrlException "
    raise start_pytomo.MaxUrlException


def patch_do_crawl():
    "Function to patch the namespace of do_crawl"
    mock_input_links = set(['http://www.youtube.com/watch?v=3NGSU2PM9dA',
                                 'http://www.youtube.com/watch?v=6T1uo2UytjQ',
                                 'http://www.youtube.com/watch?v=825o9oskWnQ',
                                 'http://www.youtube.com/watch?v=GnxGZ9jeuP8',
                                 'http://www.youtube.com/watch?v=cbaIN_K1FEg',
                                 'http://www.youtube.com/watch?v=iwYZ3LHHERI',
                                 'http://www.youtube.com/watch?v=jrkzBpeybkc',
                                 'http://www.youtube.com/watch?v=owIWfy8rAEM',
                                 'http://www.youtube.com/watch?v=xQtNFkeoGS0',
                                 'http://www.youtube.com/watch?v=yYsOnfN5tIU'])

    mock_next_round_urls = set(['http://www.youtube.com/watch?v=05jtR9fZAnQ',
                                  'http://www.youtube.com/watch?v=2uJE48aKVNo',
                                  'http://www.youtube.com/watch?v=6RM_AGSOuik',
                                  'http://www.youtube.com/watch?v=6rM-k3DjKnY',
                                  'http://www.youtube.com/watch?v=7qYfsPxfnfE',
                                  'http://www.youtube.com/watch?v=BQlq6B0ZFHY',
                                  'http://www.youtube.com/watch?v=DeOEipkkFQk',
                                  'http://www.youtube.com/watch?v=E1IIZh2TmXI',
                                  'http://www.youtube.com/watch?v=EwJ7ePes74U',
                                  'http://www.youtube.com/watch?v=FPHUvUjdWXo',
                                  'http://www.youtube.com/watch?v=HaGdxy5erI0',
                                  'http://www.youtube.com/watch?v=J-Z6Pjt49uA',
                                  'http://www.youtube.com/watch?v=Lm8GlXSNLTA',
                                  'http://www.youtube.com/watch?v=MyNSx7TXVqE',
                                  'http://www.youtube.com/watch?v=N118ePe_uzk',
                                  'http://www.youtube.com/watch?v=Q3M8whx1gj4',
                                  'http://www.youtube.com/watch?v=SKxge0n1ROg',
                                  'http://www.youtube.com/watch?v=Tlne2K2hEB4',
                                  'http://www.youtube.com/watch?v=YgFyi74DVjc',
                                  'http://www.youtube.com/watch?v=bktApGw648E',
                                  'http://www.youtube.com/watch?v=dooKpdIwwR4',
                                  'http://www.youtube.com/watch?v=e1h5TzdTq0o',
                                  'http://www.youtube.com/watch?v=gibd62eIjLM',
                                  'http://www.youtube.com/watch?v=hORUSzOvUfM',
                                  'http://www.youtube.com/watch?v=i70lh4UmujY',
                                  'http://www.youtube.com/watch?v=jZm7RluYWdI',
                                  'http://www.youtube.com/watch?v=k7q3vAR_OfQ',
                                  'http://www.youtube.com/watch?v=mkpFCIyhQT8',
                                  'http://www.youtube.com/watch?v=pB-uOGgSQIc',
                                  'http://www.youtube.com/watch?v=tCEAn1BzJWw',
                                  'http://www.youtube.com/watch?v=ta7kLbUXEeM',
                                  'http://www.youtube.com/watch?v=u4usQWXc1yQ',
                                  'http://www.youtube.com/watch?v=vYiMI32YaF8',
                                  'http://www.youtube.com/watch?v=ySX3P8S0avA',
                                  'http://www.youtube.com/watch?v=znCPgldRWTc'])

    lib_youtube_api._get_popular_links =  lib_youtube_api.get_popular_links
    lib_youtube_api.get_popular_links =  (
                    lambda time, max_results: mock_input_links)
    lib_cache_url._get_next_round_urls = lib_cache_url.get_next_round_urls
    lib_cache_url.get_next_round_urls = (
                     lambda input_links, max_per_page, max_per_url:
                                        mock_next_round_urls)
    start_pytomo._crawl_links = start_pytomo.crawl_links
    start_pytomo.crawl_links = raise_maxurlexception
    config_pytomo.PLOT = False

def unpatch_do_crawl():
    "Function to clear namespace of do_crawl"
    lib_youtube_api.get_popular_links =  lib_youtube_api._get_popular_links
    delattr(lib_youtube_api, '_get_popular_links')
    lib_cache_url.get_next_round_urls = lib_cache_url._get_next_round_urls
    delattr(lib_cache_url, '_get_next_round_urls')

@ntools.with_setup(patch_do_crawl, unpatch_do_crawl)
def test_do_crawl():
    "Function to test do_crawl"
    mock_file_name = 'mock_file'
    mock_file = open(mock_file_name, 'w+r')
    data_base = lib_database.PytomoDatabase('mock_db.db')
    data_base.create_pytomo_table('mock_table')
    start_pytomo.do_crawl(mock_file, 'mock_db.db', 'mock_time_stamp')


# Test for log_provider
EXPECTED_PROVIDER = 'Mock_test_provider'
def patch_log_provider():
    "Function to patch the namespace of log_provider"
    start_pytomo._prompt_provider = start_pytomo.prompt_provider
    start_pytomo.prompt_provider = lambda x, y: EXPECTED_PROVIDER

def unpatch_log_provider():
    "Function to clear the namespace of log_provider"
    start_pytomo.prompt_provider = start_pytomo._prompt_provider
    delattr(start_pytomo, "_prompt_provider")

@ntools.with_setup(patch_log_provider, unpatch_log_provider)
def test_log_provider():
    "Function to test log_provider"
    provider = start_pytomo.log_provider(5)
    ntools.assert_equals(provider, EXPECTED_PROVIDER )

# Test for main
EXPECTED_OUTPUT = """Usage: nosetests [-r max_rounds] [-u max_crawled_url]
[-p max_per_url] [-P max_per_page] [-t time_frame] [-n ping_packets] [-D
download_time] [-B buffering_video_duration] [-M min_playout_buffer_size] [-x]
[-L log_level]

Options:
  -h, --help            show this help message and exit
  -r MAX_ROUNDS         Max number of rounds to perform (default 100)
  -u MAX_CRAWLED_URL    Max number of urls to visit (default 5000)
  -p MAX_PER_URL        Max number of related urls from each page (default 2)
  -P MAX_PER_PAGE       Max number of related videos from each page (default
                        30)
  -t TIME_FRAME         Timeframe for the most popular videos to fetch at
                        start of crawl put 'today', 'week', 'month' or
                        'all_time' (default 'week')
  -n PING_PACKETS       Number of packets to be sent for each ping (default 1)
  -D DOWNLOAD_TIME      Download time for the video (default 8.000000)
  -B BUFFERING_VIDEO_DURATION
                        Buffering video duration (default 3.000000)
  -M MIN_PLAYOUT_BUFFER_SIZE
                        Minimum Playout Buffer Size (default 1.000000)
  -x                    Do NOT store public IP address of the machine in the
                        logs
  -L LOG_LEVEL          The log level setting for the Logging module.Choose
                        from: 'DEBUG', 'INFO', 'WARNING', 'ERROR' and
                        'CRITICAL' (default 'DEBUG')
  --http-proxy=PROXIES  in case of http proxy to reach Internet (default
  None)"""

# Test for main and option parser
def patch_main_help():
    "Patch the namespace of main() to check for -h option"
    start_pytomo._prompt_start_crawl = start_pytomo.prompt_start_crawl
    start_pytomo.prompt_crawl = lambda : 'Y'
    sys._stdout = sys.stdout
    out = StringIO()
    sys.stdout = out
    sys.argv[1] = '-h'

def unpatch_main_help():
    "Clear the namespace of main() "
    start_pytomo.prompt_start_crawl = start_pytomo._prompt_start_crawl
    delattr(start_pytomo, '_prompt_start_crawl')
    sys.stdout = sys._stdout
    delattr(sys, '_stdout')

@ntools.with_setup(patch_main_help, unpatch_main_help)
def test_main_help():
    """Test for main() only '-h' option implemented(helps to verify
    documentation)
    """
    try:
        start_pytomo.main()
    except SystemExit, e:
        "Option Parser does a system.exit() hence we need to catch it "
        ntools.assert_equals(type(e), type(SystemExit()))
        ntools.assert_equals(e.code, 0)
    output = sys.stdout.getvalue().strip()
    output = output.replace(' ', '')
    output = output.replace('\n','')
    expected_output = EXPECTED_OUTPUT.replace(' ', '')
    expected_output = expected_output.replace('\n','')
    ntools.assert_equals(output, expected_output)


"""
# Test for main and option parser
def patch_main():
    "Function to patch the name space of main"
    start_pytomo._prompt_start_crawl = start_pytomo.prompt_start_crawl
    start_pytomo.prompt_crawl = lambda : 'Y'
    sys._stdout = sys.stdout
    out = StringIO()
    sys.stdout = out
    sys.argv[1] = ''

def unpatch_main():
    "Fuction to clear the namespace of main"
    start_pytomo.prompt_start_crawl = start_pytomo._prompt_start_crawl
    delattr(start_pytomo, '_prompt_start_crawl')
    sys.stdout = sys._stdout
    delattr(sys, '_stdout')

@ntools.with_setup(patch_main, unpatch_main)
def test_main():
    try:
        start_pytomo.main()
    except SystemExit, ex:
        #Option Parser does a system.exit() hence we need to catch it.
        ntools.assert_equals(type(ex), type(SystemExit()))
        ntools.assert_equals(ex.code, 0)
    sys.stdout.write('Y')
    sys.stdout.write('Mock')
    output = sys.stdout.getvalue().strip()
    ntools.assert_equals(output, None)
"""


