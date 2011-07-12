#!/usr/bin/env python
"""A simple HTTP server

To start the server:

    python delayserver.py

Ipython Run:
    import BaseHTTPServer
    from delayserver import MyHTTPRequestHandler
    http = BaseHTTPServer.HTTPServer( ('localhost', 8000),
        MyHTTPRequestHandler)
    http.serve_forever()

Testing the lib_youtube_download:

    import urllib2
    proxy_support = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)

import pytomo.start_pytomo as start_pytomo
start_pytomo.configure_log_file('download_status.log')
import pytomo.lib_youtube_download as lib_youtube_download
fd = lib_youtube_download.FileDownloader(100)
fd._do_download('http://localhost:8000/6Dh2azWAHas-34.flv')


Note: While using localhost make sure that Firefox preferences are set
to use 'NO PROXY' for localhost.

"""
# for python 2.5
from __future__ import with_statement

import BaseHTTPServer
import sys
import urllib2
import os

#import thread
import tempfile
sys.path.append('..')
import pytomo

HTTP_OK = 200

SMALL_DATA_BLOCK = 100

INTERMEDIATE_HOSTNAME = 'localhost'
#HOSTNAME = '10.193.224.128'
PORT_NUMBER = 8002
WRITTENBYTES = 0
VIDEO_SERVER_URL = 'http://s-spo-hti:8001'
BLOCK_SIZE = 1024

STD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.12) \
    Gecko/20101028 Firefox/3.6.12',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.  8',
    'Accept-Language': 'en-us,en;q=0.5',
}


class Streamer(object):
    "Mock data stream that has info, read and write functions"
    _fifo = None
    _info = None
    _rf_int = None
    _wf_int = None

    def __init__(self, fifo, info):
        self._fifo = fifo
        self._info = info
        os.mkfifo(fifo)
        self._rf_int = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
        self._wf_int = os.open(fifo, os.O_WRONLY)

    def info(self):
        "Returns the info object"
        return self._info

    def read(self, data_length):
        """Function to read the data from the stream.
        Reads at most data_length bytes"""
        current_data = None

        while not current_data:
            # Hold untill you get the data
            # But need to check for the length of data ??
            try:
                data = os.read(self._rf_int, data_length)
            except OSError:
                #FIXME: Is this good????
                pass

    def write(self, data):
        "Function to write data to he stream"
        os.write(self._wf_int, data)

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    "HTTPHandler to serve the video"

    def do_GET(self):
        "Function to handle the get message"
        request = self.path.strip("/").split('?')[0]
        shutdown = False
        self.write_video(request)

    def write_video(self, request):
        "Function to service the webpages"
        video_url = VIDEO_SERVER_URL + '/' + request
        status_code, video_data = self.connect_video_server(video_url)
        self.send_response(HTTP_OK)
        self.send_header('ContentType', 'text/plain;charset=utf-8')
        self.send_header('Content-Length', str(os.path.getsize(request)))
        self.send_header('Pragma', 'no-cache' )
        self.end_headers()
        output = self.wfile
        temp_file = None
        size = os.path.getsize(request)
        written_bytes = 0
        common_data = video_data.read(SMALL_DATA_BLOCK)
        output.write(common_data)

        if (video_data.geturl().find('flv') >= 0
            or video_data.geturl().find('mp4') >= 0):
            # Need to write to process_download
            # addinfourl: But does not provide write method???
            file_downloader = pytomo.lib_youtube_download.FileDownloader(200)
            #temp_file = tempfile.NamedTemporaryFile()
            #temp_stream = open(temp_file.name, 'r+')
            #Converting a file oblect to a HTTPResponse oblect
            #download_stream = urllib.addinfourl(temp_file, video_data.info(),
            #                  video_data.geturl())
            #setattr(temp_stream, 'info', lambda: video_data.info())
            #temp_stream.geturl = lambda: video_data.geturl()
            #temp_stream.write(common_data)

            #meta_file = tempfile.NamedTemporaryFile()
            temp_fifo_dir = tempfile.mkdtemp()
            fifo_path = os.path.join(temp_fifo_dir, 'fifo_2')
            data_stream = Streamer(fifo_path, video_data.info())
            written_bytes += SMALL_DATA_BLOCK
            print "Calling process download in new thread"
            #thread.start_new_thread(file_downloader.process_download,
            #                        (data_stream, meta_file.name))

        # serving the reqest from the browser
        print video_data.geturl()
        print video_data.info()
        while written_bytes < size:
            common_data = video_data.read(SMALL_DATA_BLOCK)
            # write to web_page
            output.write(common_data)
            # write to process_download data_stream
            if not (video_data.geturl().find('flv') or
                    video_data.geturl().find('mp4')) == -1:
                data_stream.write(common_data)
            if temp_file:
                temp_file.write(common_data)
            written_bytes += SMALL_DATA_BLOCK

    def connect_video_server(self, url):
        """ Connect to the video server and return the data stream """
        data = None
        status_code = None
        request = urllib2.Request(url, None, STD_HEADERS)
        count = 0
        max_retries = 0
        while count < max_retries:
            # Establish connection
            try:
                data = urllib2.urlopen(request)
            except (urllib2.HTTPError, ), err:
                if (err.code < 500 or err.code >= 600) and err.code != 416:
                    # Unexpected HTTP error
                    raise
                elif err.code == 416:
                    # Unable to resume (requested range not satisfiable)
                    try:
                        # Open the connection again without the range header
                        data = urllib2.urlopen(request)
                    except (urllib2.HTTPError, ), err:
                        if err.code < 500 or err.code >= 600:
                            raise
            # Retry
            count += 1
        if count > max_retries:
            self.log.message(u'ERROR: Unable to connect to video server'
                             'giving up after %d retries' % count)
        data = urllib2.urlopen(request)
        return status_code, data

def main(stop_after_flv=False):
    "Function to start server"
    pytomo.start_pytomo.configure_log_file('intermediate_server.log')
    proxy_support = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    http_server = BaseHTTPServer.HTTPServer((INTERMEDIATE_HOSTNAME,
                                             PORT_NUMBER),
                                            MyHTTPRequestHandler)
    http_server.stop_after_flv = stop_after_flv
    print ("Intermediate host Listening on ", PORT_NUMBER,
           " - press ctrl-c to stop")
    http_server.serve_forever()

if __name__ == "__main__":
    sys.exit(main())
