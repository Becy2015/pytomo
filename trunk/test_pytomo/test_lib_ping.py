#!/usr/bin/env python
"""
   Mock test module for lib_ping.py
"""
import nose.tools as ntools
from ..pytomo import lib_ping
from ..pytomo import start_pytomo
from ..pytomo import config_pytomo
import os
import platform

import doctest
doctest.testmod(lib_ping)

# Mock test for ping_ip
def return_ping():
    "Function that returns the ping values"
    machine = platform.system().lower()
    if machine.startswith('linux'):
        rtt_value = ["rtt min/avg/max/mdev = 9.99/9.99/9.99/9.99 ms"]
    if machine.startswith('windows') or machine.startswith('microsoft'):
        if 'LANG' in os.environ and os.environ['LANG'] == 'FR':
            rtt_value = ["Minimum = 9.99ms, Maximum = 9.99ms, Moyenne = 9.99ms"]
        else:
            rtt_value = ["Minimum = 9.99ms, Maximum = 9.99, Average = 9.99ms"]
    if machine.startswith('darwin'):
        rtt_value = ["round-trip min/avg/max/stddev =  9.99/9.99/9.99/9.99 ms"]
    return rtt_value

def patch_ping_ip():
    """Function to patch the namespace of the functions to be replaced.
    Returns a mock RTT stats string"""
    start_pytomo.configure_log_file('mock')
    config_pytomo.SYSTEM = platform.system().lower()
    os._popen = os.popen
    os.popen = lambda *args : return_ping()

def patch_ping_ip_none():
    "Function to patch the namespace of the functions to be replaced"
    os._popen = os.popen
    os.popen = lambda *args: "Ping not allowed"

def unpatch_ping_ip():
    "Function to unpatch the namespace of the functions to be replaced"
    os.popen = os._popen
    delattr(os, '_popen')

@ntools.with_setup(patch_ping_ip, unpatch_ping_ip)
def test_ping_ip():
    "The module to setup the test and run the test for patch_ip"
    ip_address = '127.0.0.1'
    packets = 5
    res = lib_ping.ping_ip(ip_address, packets)
    expected_res = [9.99, 9.99, 9.99]
    ntools.assert_equals(res, expected_res)

@ntools.with_setup(patch_ping_ip_none, unpatch_ping_ip)
def test_ping_ip_none():
    "Module to setup and run the test ping_none"
    ip_address = '10.10.10.10'
    packets = 5
    res = lib_ping.ping_ip(ip_address, packets)
    ntools.assert_equals(res, None)
#
#def patch_ping_ip_unknown_system():
#    "Function to patch the namespace of the functions to be replaced"
#    platform._system = platform.system
#    platform.system = lambda x: 'UNKNOWN'
#
#def unpatch_ping_ip_unknown_system():
#    "Function to clear namespace"
#    platform.system = platform._system
#    delattr(platform, '_system')
#
#
#@ntools.with_setup(patch_ping_ip_unknown_system, unpatch_ping_ip_unknown_system)
#def test_ping_ip_unknown():
#    "Module to setup and run the test ping_unknown system"
#    ip_address = '10.10.10.10'
#    packets = 5
#    res = lib_ping.ping_ip(ip_address, packets)
#    ntools.assert_equals(res, None)
#
