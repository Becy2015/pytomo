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

"""

# for python 2.5
from __future__ import with_statement

import time
import BaseHTTPServer
import sys
import os

sys.path.append('..')
import pytomo
#from lib_youtube_download import get_data_duration

HOSTNAME = 'localhost'
#HOSTNAME = '10.193.224.128'
PORT_NUMBER = 8001
WRITTENBYTES = 0
# Interruption duration in seconds
INTERUPTIONS_DURATION = 15
# In bytes
UNINTERRUPTED_STREAM_SIZE =  3669363
#UNINTERRUPTED_STREAM_SIZE = 20000


INITIAL_SLEEP = 10
FIRST_BLOCK = 523264

#UNINTERRUPTED_STREAM_SIZE = 10240

FLV_FILES = ['7UCm6uyzNE8-18.mp4', '7UCm6uyzNE8-34.flv',
             '7UCm6uyzNE8-5.flv',
             '7UCm6uyzNE8.mp4', '7UCm6uyzNE8-22.mp4', '7UCm6uyzNE8-35.flv',
             '7oVwankxKj8-18.mp4', '7oVwankxKj8-34.flv', '7oVwankxKj8-37.mp4',
             '7oVwankxKj8-22.mp4', '7oVwankxKj8-35.flv', '7oVwankxKj8-5.flv',
             'LjMkNrX60mA-18.mp4', 'LjMkNrX60mA-34.flv', 'LjMkNrX60mA-5.flv',
             'LjMkNrX60mA-22.mp4', 'LjMkNrX60mA-35.flv', '6Dh2azWAHas-34.flv',
             'Cv82TESa5WM-34.flv', 'Cv82TESa5WM-35.flv', 'Cv82TESa5WM-5.flv',
             'EbCoDf44oCE-18.mp4', 'EbCoDf44oCE-34.flv', 'EbCoDf44oCE-37.mp4',
             'EbCoDf44oCE-22.mp4', 'EbCoDf44oCE-35.flv', 'EbCoDf44oCE-5.flv',
             'eHQG6-DojVw-18.mp4', 'eHQG6-DojVw-34.flv', 'eHQG6-DojVw-5.flv',
             '7oVwankxKj8-37.mp4', 'LjMkNrX60mA-35.flv', 'XjwIVe5D290-35.flv',
             'XjwIVe5D290-34.flv', 'XjwIVe5D290-18.mp4', 'XjwIVe5D290-5.flv',
             '6PKQE8FM2Uw-34.flv', 'eHQG6-DojVw-18.mp4', 'To2HY9i4ePA-37.mp4',
             '4eTMDkbS0fc-22.mp4', 'a5irTX82olg-35.flv',
             'jzIBZQkj6SY-35.flv', 'XRwX9oCaE9Q-34.flv',
             'XRwX9oCaE9Q-35.flv', 'XRwX9oCaE9Q-5.flv', 'nPoQBwuwE2A-5.flv',
             'nPoQBwuwE2A-35.flv', 'nPoQBwuwE2A-34.flv',
             'jzIBZQkj6SY-18.mp4', 'jzIBZQkj6SY-35.flv', 'jzIBZQkj6SY-34.flv',
             'jzIBZQkj6SY-5.flv']
PAGES = ['html_pages/index.html', 'html_pages/embedding_page.html',
         'html_pages/topindex.html',
         'jwplayer.js', 'html_pages/swfobject.js', 'html_pages/index1.html',
        'html_pages/7oVwankxKj8.html', 'html_pages/7UCm6uyzNE8.html',
        'html_pages/LjMkNrX60mA.html', 'html_pages/EbCoDf44oCE.html',
        'html_pages/eHQG6-DojVw.html', 'html_pages/jzIBZQkj6SY.html',
        'html_pages/XjwIVe5D290.html']

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    "HTTPHandler to serve the video"

    def do_GET(self):
        "Function to handle the get message"
        request = self.path.strip("/").split('?')[0]
        shutdown = False
        if request in FLV_FILES:
            valid_request = True
            write_method = slow_write
            kwargs = {'int_dur': INTERUPTIONS_DURATION,
                      'unint_size': UNINTERRUPTED_STREAM_SIZE}
            if self.server.stop_after_flv:
                shutdown = True
        elif request in PAGES:
            valid_request = True
            write_method = normal_write
            kwargs = {}
        else:
            valid_request = False
        if (valid_request == False):
            self.send_error(404)
            return
        self.send_response( 200 )
        self.send_header('ContentType', 'text/plain;charset=utf-8')
        self.send_header('Content-Length', str(os.path.getsize(request)))
        self.send_header('Pragma', 'no-cache' )
        self.end_headers()
        duration = write_method(self.wfile, request, **kwargs)
        self.log_message('Request took %f seconds', duration)
        if shutdown:
            self.server.shutdown()

def normal_write(output, request):
    "Function to write the video onto output stream"
    with open(request, 'r') as request_file:
        start_time = time.time()
        output.write(request_file.read())
        now = time.time()
        output.flush()
    return now - start_time


def slow_write(output, request, int_dur=INTERUPTIONS_DURATION,
               unint_size=UNINTERRUPTED_STREAM_SIZE):
    """Function to write the video onto output stream with interruptions in
    the stream
    """
    #first_block = int(get_initial_nb_bytes(request, initial_dur=2100))
    first_block = FIRST_BLOCK
    writtenbytes = 0
    current_stream = 0
    block_size = 1024
    with open(request, 'r') as request_file:
        start_time = time.time()
        data = request_file.read(first_block + 20)
        print "Written first_block of size:", first_block
        output.write(data)
        time.sleep(INITIAL_SLEEP)
        current_stream += len(data)
        data = request_file.read(block_size)
        while (data != ''):
            now = time.time()
            if current_stream > unint_size:
                time.sleep(int_dur)
                #print "Writtenbytes till now", writtenbytes
                current_stream = 0
            output.write(data)
            data = request_file.read(block_size)
            current_stream += len(data)
            writtenbytes += len(data)
        now = time.time()
        output.flush()
    print 'Served %d bytes of file: %s' % (writtenbytes, request)
    return now - start_time

def get_initial_nb_bytes(flv_file, initial_dur=2000):
    """Return the amount of bytes necessary to write only up to initial_dur
    seconds
    """
    #return pytomo.lib_youtube_download.get_initial_playback_flv(flv_file,
      #                                                          initial_dur)

    # total_size = os.path.getsize(flv_file)
    # total_duration, _ = pytomo.lib_youtube_download.get_data_duration(flv_file)
    # return initial_dur * total_size / total_duration

def main(stop_after_flv=False):
    "Function to start server"
    http_server = BaseHTTPServer.HTTPServer((HOSTNAME, PORT_NUMBER),
                                            MyHTTPRequestHandler)
    http_server.stop_after_flv = stop_after_flv
    print "Listening on ", PORT_NUMBER, " - press ctrl-c to stop"
    http_server.serve_forever()

if __name__ == "__main__":
    sys.exit(main())

