#!/usr/bin/env python

"""
   Mock test module for lib_youtube_download.py
   In order for pylint to not show 'Module 'nose.tools' has no
   'assert_equals' member'

   Use:
   pylint --ignored-classes=nose.tools test_lib_youtube_download.py
#

"""

#from __future__ import absolute_import
import nose.tools as ntools
from ..pytomo import lib_youtube_download
from ..pytomo import start_pytomo
import urllib2
from cgi import parse_qs
import doctest
doctest.testmod(lib_youtube_download)

FLASH_FILE = 'OdF-oiaICZI.flv'
VIDEO_ID = 'OdF-oiaICZI'
start_pytomo.configure_log_file('mock')
# Mock test for the FileDownloader class
# Test for process_info
#
expected_download_time = 30.03
VIDEO_URL =  ''.join(('http://v7.lscache8.c.youtube.com/videoplayback?',
               'sparams=id%2Cexpire%2Cip%2Cipbits%2Citag%2Calgorithm%2Cbu',
                         'rst%2Cfactor&fexp=901904&algorithm=throttle-fact',
                         'or&itag=34&ipbits=8&burst=40&sver=3&signature=C2C',
                         'A52DF6A10F2C132DAA297E16972E7007A250D.9A48',
                         '6A89ABC9C278564505B72D2229B5994DA1B0&expire=130',
                         '3311600&key=yt1&ip=193.0.0.0&factor=1.25',
                         '&id=39d17ea226880992'))
INFO_DICT = {'ext': u'flv',
             'format': u'34',
             'id': unicode(VIDEO_ID),
             'url':VIDEO_URL }

def patch_process_info():
    "Function to patch the namepace of process_info"
    lib_youtube_download.FileDownloader.__do_download = (
        lib_youtube_download. FileDownloader._do_download)
    lib_youtube_download.FileDownloader._do_download = (
        lambda x, y: (200, expected_download_time))

def unpatch_process_info():
    "Function to clear the namepace of process_info"
    lib_youtube_download.FileDownloader._do_download = (
        lib_youtube_download.FileDownloader.__do_download)
    delattr(lib_youtube_download.FileDownloader, '__do_download')

@ntools.with_setup(patch_process_info, unpatch_process_info)
def test_process_info():
    "Testing process info"
    filedownloader = lib_youtube_download.FileDownloader(30)
    d_time = filedownloader.process_info(INFO_DICT)
    ntools.assert_equals(d_time, expected_download_time)

# Test for IOError in process_info
def patch_process_info_ioerror():
    "Function to patch the namepace of process_info"
    lib_youtube_download.FileDownloader.__do_download = (
        lib_youtube_download. FileDownloader._do_download)
    lib_youtube_download.FileDownloader._do_download = raise_ioerror

def raise_ioerror(obj, url):
    "Function to raice IOError"
    raise IOError

@ntools.raises(lib_youtube_download.UnavailableVideoError)
@ntools.with_setup(patch_process_info_ioerror, unpatch_process_info)
def test_process_info_ioerror():
    "Testing process info with IOError"
    filedownloader = lib_youtube_download.FileDownloader(30)
    d_time = filedownloader.process_info(INFO_DICT)
    ntools.assert_equals(d_time, expected_download_time)


# Test for OSError in process_info
def patch_process_info_oserror():
    "Function to patch the namepace of process_info"
    lib_youtube_download.FileDownloader.__do_download = (
        lib_youtube_download. FileDownloader._do_download)
    lib_youtube_download.FileDownloader._do_download = raise_oserror

def raise_oserror(obj, url):
    "Function to raice OSError"
    raise OSError

@ntools.raises(lib_youtube_download.UnavailableVideoError)
@ntools.with_setup(patch_process_info_oserror, unpatch_process_info)
def test_process_info_oserror():
    "Testing process info with OSError"
    filedownloader = lib_youtube_download.FileDownloader(30)
    d_time = filedownloader.process_info(INFO_DICT)
    ntools.assert_equals(d_time, expected_download_time)


# Test for HTTPException in process_info
def patch_process_info_httpexceptn():
    "Function to patch the namepace of process_info"
    lib_youtube_download.FileDownloader.__do_download = (
        lib_youtube_download. FileDownloader._do_download)
    lib_youtube_download.FileDownloader._do_download = raise_httpexception

def raise_httpexception(obj, url):
    "Function to raice OSError"
    import httplib
    raise httplib.HTTPException()

@ntools.raises(lib_youtube_download.DownloadError)
@ntools.with_setup(patch_process_info_httpexceptn, unpatch_process_info)
def test_process_info_httpexception():
    "Testing process info with OSError"
    filedownloader = lib_youtube_download.FileDownloader(30)
    d_time = filedownloader.process_info(INFO_DICT)
    ntools.assert_equals(d_time, expected_download_time)

########################################################
# Test for establish_connection
def fake_urlopen_est_conn(request):
    "Fake urlopen for 'establish_connection' method "
    url = request.get_full_url()
    class data:
        def geturl(self):
            return url
    if not url.find('v6') == -1:
        return data()
    elif not url.find('v7') == -1:
        raise urllib2.HTTPError(url = url, msg = 'mock_test', code=606,
                               hdrs = None, fp=None)
    elif not url.find('v8') == -1:
        raise urllib2.HTTPError(url = url, msg = 'mock_test', code=500,
                                hdrs = None,fp = None)
    elif not url.find('v9') == -1:
        raise urllib2.HTTPError(url = url, msg = 'mock_test', code = 416,
                                hdrs = None, fp = None)



def patch_establish_conection():
    "Patch function for YoutubeIE.get_video_info"
    urllib2._urlopen = urllib2.urlopen
    urllib2.urlopen = fake_urlopen_est_conn

def unpatch_establish_connection():
    "Function to remove the patch on the namespace"
    urllib2.urlopen = urllib2._urlopen
    delattr(urllib2, '_urlopen')

@ntools.with_setup(patch_establish_conection, unpatch_establish_connection)
def test_establish_connection():
    "Test for successful case of establish connection"
    filedownloader = lib_youtube_download.FileDownloader(30)
    data_1 = filedownloader.establish_connection('http://v6.lscache.com')
    ntools.assert_equals(200, data_1[0])



@ntools.raises(urllib2.HTTPError)
@ntools.with_setup(patch_establish_conection, unpatch_establish_connection)
def test_establish_connection_606():
    "Test for HTTP 606 Error of establish connection"
    filedownloader = lib_youtube_download.FileDownloader(30)
    filedownloader.establish_connection('http://v7.lscache.com')

@ntools.with_setup(patch_establish_conection, unpatch_establish_connection)
def test_establish_connection_500():
    "Test for 500 error of establish connection"
    filedownloader = lib_youtube_download.FileDownloader(30)
    data = filedownloader.establish_connection('http://v8.lscache.com')
    ntools.assert_equals(data, (None,None))

@ntools.raises(urllib2.HTTPError)
@ntools.with_setup(patch_establish_conection, unpatch_establish_connection)
def test_establish_connection_416():
    "Test for 416 Error of establish connection"
    filedownloader = lib_youtube_download.FileDownloader(30)
    filedownloader.establish_connection('http://v9.lscache.com')

# Mock test for the Youtube_IE class
def fake_urlopen(request):
    "fake urlopen: This serves only one page Video id = VIDEO_ID "
    url = request.get_full_url()
    if url.find(VIDEO_ID) == -1:
        return open('video_info_webpage_not_available.txt', 'r')
    elif url.find('&el=embedded'):
        return open('video_info_webpage_embedded.txt', 'r')
    elif url.find('&el=detailpage'):
        return open('video_info_webpage_detailpage.txt', 'r')
    elif url.find('&el=vevo'):
        return open('video_info_webpage_vevo', 'r')
    else:
        return open('video_info_webpage_none.txt', 'r')

def patch_get_video_info_available():
    "Patch function for YoutubeIE.get_video_info"
    urllib2._urlopen = urllib2.urlopen
    urllib2.urlopen = fake_urlopen

def unpatch_get_video_info():
    "Function to remove the patch on the namespace"
    urllib2.urlopen = urllib2._urlopen
    delattr(urllib2, '_urlopen')

@ntools.with_setup(patch_get_video_info_available, unpatch_get_video_info)
def test_get_video_info():
    "Test for succesfull get_video_info"
    youtube_ie = lib_youtube_download.get_youtube_info_extractor()
    video_info = youtube_ie.get_video_info(VIDEO_ID)
    expected_token = ['vjVQa1PpcFM06tONmnETusa1ojFpPElZPmq0TD4gZ34=']
    ntools.assert_equal(video_info['token'], expected_token)

@ntools.raises(lib_youtube_download.DownloadError)
@ntools.with_setup(patch_get_video_info_available, unpatch_get_video_info)
def test_get_video_info_fail():
    "Test for unsucessful get_video_info"
    video_id = 'RcmKbTR--iA' # video-id not supported by fake server
    youtube_ie = lib_youtube_download.get_youtube_info_extractor()
    youtube_ie.get_video_info(video_id)

# Test for video_url_list
def test_test_video_url_list():
    "Test for YoutubeIE.get_video_url_list"
    import urllib
    video_info_file = open('video_info_webpage_none.txt', 'r')
    video_info_webpage = video_info_file.read()
    video_info = parse_qs(video_info_webpage)
    video_token = urllib.unquote_plus(video_info['token'][0])
    youtube_ie = lib_youtube_download.get_youtube_info_extractor()
    video_url_list = youtube_ie.get_video_url_list(VIDEO_ID, video_token,
                                                   video_info)
    """    expected_video_url_list = [('34',
                 ''.join(('http://v7.lscache8.c.youtube.com/videoplayback?',
               'sparams=id%2Cexpire%2Cip%2Cipbits%2Citag%2Calgorithm%2Cbu',
                         'rst%2Cfactor&fexp=901904&algorithm=throttle-fact',
                         'or&itag=34&ipbits=8&burst=40&sver=3&signature=C2C',
                         'A52DF6A10F2C132DAA297E16972E7007A250D.9A48',
                         '6A89ABC9C278564505B72D2229B5994DA1B0&expire=130',
                         '3311600&key=yt1&ip=193.0.0.0&factor=1.25',
                         '&id=39d17ea226880992')))]
    """

    expected_video_url_list = [('34', VIDEO_URL)]
    ntools.assert_equals(video_url_list, expected_video_url_list)

    #Test with another webpage with the same video_id
    video_info_file = open('video_info_webpage_vevo.txt', 'r')
    video_info_webpage = video_info_file.read()
    video_info = parse_qs(video_info_webpage)
    video_token = urllib.unquote_plus(video_info['token'][0])
    youtube_ie = lib_youtube_download.get_youtube_info_extractor()
    video_url_list = youtube_ie.get_video_url_list(VIDEO_ID, video_token,
                                                   video_info)
    expected_video_url_list = [ ('34',
            ''.join(('http://v7.lscache8.c.youtube.com/videoplayback?',
                    'sparams=id%2Cexpire%2Cip%2Cipbits%2Citag%2Calgorithm%2Cb',
                    'urst%2Cfactor&fexp=909511%2C904531&algorithm=throttle-f',
                    'actor&itag=34&ipbits=8&burst=40&sver=3&signature=C2CA52D',
                    'F6A10F2C132DAA297E16972E7007A250D.9A486A89ABC9C278',
                     '564505B72D2229B5994DA1B0&expire=1303311600&key=yt1&',
                     'ip=193.0.0.0&factor=1.25&id=39d17ea226880992')))]
    ntools.assert_equals(video_url_list, expected_video_url_list)
"""
# Test for _real_extract
def fake_get_video_info(video_id):
    if video_id = '':
        video_info_webpage = open('video_info_webpage_none', 'r')
        video_info = parse_qs(video_info_webpage)
        return video_info

def patch__real_extract():
    "Function to patch the namspace for _real_extract"
    lib_youtube_download.YoutubeIE._get_video_info = (
        lib_youtube_download.YoutubeIE.get_video_info)
    lib_youtube_download.YoutubeIE.get_video_info = fake_get_video_info

def unpatch__real_extract():
    lib_youtube_download.YoutubeIE.get_video_info = (
        lib_youtube_download.YoutubeIE._get_video_info)
    delattr(lib_youtube_download.YoutubeIE, '_get_video_info')

@ntools.with_setup(patch__real_extract, unpatch__real_extract)
def test__real_extract():
    youtube_ie = lib_youtube_download.get_youtube_info_extractor()
    video_url_list = youtube_ie.get_video_url_list(video_id, video_token,

"""


# Test for get_data_duration
def test_get_data_duration():
    "Test for get_data_duration"
    res = lib_youtube_download.get_data_duration(FLASH_FILE)
    ntools.assert_equals(res, (287.48700000000002, 'flv'))

# Mock test for get_youtube_cache_url. It is network independent but still
# dependent on the InfoExtractor class.
SAMPLE_VIDEO_INFO = {'allow_embed': ['1'],
                      'allow_ratings': ['1'],
                      'author': ['papadoc73'],
                      'avg_rating': ['4.89416058394'],
                      'endscreen_module':
                     ['http://s.ytimg.com/yt/swfbin/endscreen-vfl29iOPn.swf'],
                      'fexp': ['903103,910002'],
                      'fmt_list':
                     ['34/320x240/9/0/115,18/320x240/9/0/115,5/320x240/7/0/0'],
                      'fmt_map':
                     ['34/320x240/9/0/115,18/320x240/9/0/115,5/320x240/7/0/0'],
                      'fmt_stream_map': [],
                      'fmt_url_map':
                     [''.join((
                    '34|http://v7.lscache8.c.youtube.com/videoplayback?',
                      'sparams=id,',
                      '18|http://v6.lscache8.c.youtube.com/videoplayback?',
                      'sparams=id,',
                      '5|http://v4.lscache7.c.youtube.com/videoplayback?',
                      'sparams=id'))],
                      'has_cc': ['False'],
                      'keywords':
                     ["tracy,chapman,mountains,o',things,archives"],
                      'leanback_module':[],
                      'length_seconds': ['288'],
                      'muted': ['0'],
                      'plid': ['AAShQiyfrNeqAFpz'],
                      'status': ['ok'],
                      'thumbnail_url':
                     ['http://i4.ytimg.com/vi/OdF-oiaICZI/default.jpg'],
                      'timestamp': ['1303205495'],
                      'title': ["TRACY CHAPMAN:  MOUNTAINS O' THINGS"],
                      'tmi': ['1'],
                      'token':
                     ['vjVQa1PpcFO1YzfkoXWY_vau8dxNTWCgbWySnW_c2xY='],
                      'track_embed': ['0'],
                      'video_id': ['OdF-oiaICZI'],
                      'vq': ['auto'],
                      'watermark': []}

def patch_get_youtube_cache_url():
    "Function to patch the namespace of dependencies"
    lib_youtube_download.YoutubeIE._get_video_info = (
        lib_youtube_download.YoutubeIE.get_video_info)
    lib_youtube_download.YoutubeIE.get_video_info = (
                        lambda x, y :SAMPLE_VIDEO_INFO)

def unpatch_get_youtube_cache_url():
    "Function to clear the patches"
    lib_youtube_download.YoutubeIE.get_video_info = (
        lib_youtube_download.YoutubeIE._get_video_info)
    delattr(lib_youtube_download.YoutubeIE, '_get_video_info')

@ntools.with_setup(patch_get_youtube_cache_url,
                   unpatch_get_youtube_cache_url)
def test_get_youtube_cache_url():
    "Test module for get_youtube_cache_url"
    url = 'http://www.youtube.com/watch?v=OdF-oiaICZI'
    res = lib_youtube_download.get_youtube_cache_url(url)
    expected_result = 'http://v7.lscache8.c.youtube.com/videoplayback?'
    ntools.assert_true(res.startswith(expected_result))

# Test for get_download_stats
def patch_get_download_stats():
    "Function to patch the namespace of dependencies"
    start_pytomo.configure_log_file('mock')
    class FakeFileDownloader(object):
        "Fake FileDownloader class that returns default values"
        def __init__(self, _):
            self.data_duration = 0,
            self.data_len = 0,
            self.encoding_rate = 0,
            self.interruptions = 0,
            self.accumulated_buffer = 0 ,
            self.accumulated_playback = 0,
            self.current_buffer = 0,
            self.max_instant_thp = 0
            self.video_type = None
        @classmethod
        def get_total_bytes(cls):
            "fake get total bytes method"
            return 1000
        def _do_download(self, ip_address_uri):
            "Fake _do_download method"
            if ip_address_uri == None:
                raise lib_youtube_download.DownloadError

            self.data_duration = 10
            self.data_len = 100
            self.encoding_rate = 10
            self.interruptions = 10
            self.accumulated_buffer = 10
            self.accumulated_playback = 10
            self.current_buffer = 1
            self.video_type = 'flv'
            return 200, 30
    lib_youtube_download._FileDownloader = (
        lib_youtube_download.FileDownloader)
    lib_youtube_download.FileDownloader = FakeFileDownloader

def unpatch_get_download_stats():
    "Function to clear the patches"
    lib_youtube_download.FileDownloader = (
        lib_youtube_download._FileDownloader)
    delattr(lib_youtube_download, '_FileDownloader')

@ntools.with_setup(patch_get_download_stats, unpatch_get_download_stats)
def test_get_download_stats():
    "Function to test get_download_stats"
    ip_address_uri = ''.join((
        'http://173.194.20.235/videoplayback?',
        'sparams=id%2Cexpire%2Cip%2Cipbits%2Citag%2Calgorithm%',
        '2Cburst%2Cfactor&fexp=903938%2C907301&algorithm=throttle-',
        'factor&itag=34&ipbits=8&burst=40&sver=3&signature=40E3F6B3E',
        '931FC0FA892438BF65876802804C812.D3F6637613F70822754C3',
        'D4C166283CBA63B47DE&expire=1303243200&key=yt1&ip=193.0.0.0',
        '&factor=1.25&id=39d17ea226880992'))
    status_code, res, redirect_url = lib_youtube_download.get_download_stats(
        ip_address_uri, 30)
    expected_result =  [30, 'flv', 10, 100, 10, 1000, 10, 10, 10, 1, 0]
    ntools.assert_equals(res, expected_result)
    res = lib_youtube_download.get_download_stats(None, 30)
    ntools.assert_false(res)

##############################################################
# Test for _do_download

def patch_do_download():
    """Function to patch the namespace or _do_download. In a fake server is
    instantiated. The default opener of urllib2 is replaced by the
    following."""
    start_pytomo.configure_log_file('http_test')
    info = {'accept-ranges': 'bytes',
             'cache-control': 'private, max-age=20576',
             'connection': 'close',
             'Content-length': '16840065',
             'content-type': 'video/x-flv',
             'date': 'Fri, 29 Apr 2011 14:12:04 GMT',
             'expires': 'Fri, 29 Apr 2011 19:55:00 GMT',
             'last-modified': 'Fri, 18 Jun 2010 12:05:11 GMT',
             'server': 'gvs 1.0',
             'via': 'my_proxy)',
             'x-content-type-options': 'nosniff'}
    def mock_response(req):
        "Mock Response class"
        if req.get_full_url() == VIDEO_URL:
            mock_file = open(FLASH_FILE)
            resp = urllib2.addinfourl(mock_file, info ,
                                      req.get_full_url())
            resp.code = 200
            resp.msg = "OK"
            return resp

    class MyHTTPHandler(urllib2.HTTPHandler):
        "Mock HTTP handler class"
        def http_open(self, req):
            print "mock opener"
            return mock_response(req)

    my_opener = urllib2.build_opener(MyHTTPHandler)
    urllib2.install_opener(my_opener)

@ntools.with_setup(patch_do_download)
def test_do_download():
    "Function to test the do_download with Mock url opener"
    filedownloader = lib_youtube_download.FileDownloader(30)
    h = filedownloader._do_download(VIDEO_URL)
    ntools.assert_not_equals(h, None)
    ntools.assert_raises(urllib2.URLError, filedownloader._do_download,
                         'http://google.com')
    ntools.assert_raises(ValueError, filedownloader._do_download,
                        'anystring')

