#!/usr/bin/env python

"""
    Module for a simple stopwatch
"""
import sys
import termios
import fcntl
import os
import time
from pprint import pprint
import webbrowser
import thread
import delayserver
from collections import defaultdict

WEBPAGE = 'http://localhost:8000/index1.html'
#WEBPAGE = 'http://localhost:8000/index.html'
VIDEO_FILE = '7UCm6uyzNE8-34.flv'

def mygetch():
    """Python recipe:
       http://love-python.blogspot.com/2010/03/
       getch-in-python-get-single-character.html"""
    file_descriptor = sys.stdin.fileno()
    oldterm = termios.tcgetattr(file_descriptor)
    new_attr = termios.tcgetattr(file_descriptor)
    new_attr[3] = new_attr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr (file_descriptor, termios.TCSANOW, new_attr)
    oldflags = fcntl.fcntl(file_descriptor, fcntl.F_GETFL)
    fcntl.fcntl(file_descriptor, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    try:
        while True:
            try:
                key_input = sys.stdin.read(1)
                return key_input
            except IOError:
                pass
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(file_descriptor, fcntl.F_SETFL, oldflags)

def report_interrupt(interrupt):
    """Format and report interruptions information"""
    pprint(interrupt)
    total_buffer_dur = 0
    for key in interrupt:
        try:
            total_buffer_dur += interrupt[key]['duration']
        except KeyError:
            print key, "had no duration"
            continue
    print "\n Total_interrupt_duration = ", total_buffer_dur

def start_delayserver():
    "Module to start delayserver"
    thread.start_new_thread(delayserver.main, (),
                            {'stop_after_flv': True})

def open_browser(webpage=None):
    "Module to open browser"
    webbrowser.open(WEBPAGE)

def stopwatch():
    "stopwatch with functions Start video, Interruptions & End of video"
    print ("Stopwatch to measure video interruptions:"
           "\n Press 'w' to start the delayserver script and open webpage in "
           "browser"
           "\n Press 's' to start"
           "\n Press 'i' to record beginning of interruption"
           "\n Press 'u' to record resumption of video after interruption"
           "\n Press 'x' or Cntrl + C to stop")
    getch = mygetch
    user_input = None
    start = None
    stop = None
    interrupt = defaultdict(dict)
    interrupt_count = 0
    while True:
        try:
            user_input = getch()
        except KeyboardInterrupt:
            break
        if user_input == 'w':
            start_delayserver()
            open_browser(WEBPAGE)
            start =  time.time()
        elif user_input == 's':
            start_delayserver()
            open_browser(WEBPAGE)
            start =  time.time()
            print "Stopwatch started"
        elif user_input == 'x':
            stop = time.time()
            if start:
                print "Stopwatch stopped."
                report_interrupt(interrupt)
                print "\n Total video duration = ", stop - start
            raise KeyboardInterrupt
        elif start and user_input == 'i':
            interrupt_count += 1
            interrupt[interrupt_count]['start'] = time.time() - start
            print "Interrupt recorded at ", interrupt[interrupt_count]
        elif start and user_input == 'u':
            if 'stop' in interrupt[interrupt_count]:
                print ''.join(("Video already resumed. Make sure you have",
                               "initialzed the interrupt"))
                continue
            interrupt[interrupt_count]['stop'] =  time.time() - start
            try:
                duration = (interrupt[interrupt_count]['stop'] -
                            interrupt[interrupt_count]['start'])
            except KeyError:
                print "key not found", interrupt[interrupt_count]
            interrupt[interrupt_count]['duration'] = duration
            print "Video continued after interrupt", interrupt[interrupt_count]
        elif start:
            print "Input not identified"
        else:
            print "stopwatch not started."

def main():
    "Main function"
    stopwatch()
    import pytomo.start_pytomo as start_pytomo
    start_pytomo.configure_log_file('download_status.log')
    import pytomo.lib_youtube_download as lib_youtube_download
    fd = lib_youtube_download.FileDownloader(100)
    thread.start_new_thread(delayserver.main, (), {'stop_after_flv': True})
    fd._do_download('http://localhost:8000/%s' % VIDEO_FILE)

if __name__ == "__main__":
    sys.exit(main())
