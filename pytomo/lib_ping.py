#!/usr/bin/env python

"""Module to generate the RTT times of a ping

 Sample for windows:

        ['\n', 'Pinging 173.194.24.138 with 32 bytes of data:\n',
        'Reply from 173.194.24.138: bytes=32 time=149ms TTL=43\n',
        'Reply from 173.194.24.138: bytes=32 time=149ms TTL=43\n',
        'Reply from 173.194.24.138: bytes=32 time=148ms TTL=43\n',
        'Reply from 173.194.24.138: bytes=32 time=149ms TTL=43\n',
        'Reply from 173.194.24.138: bytes=32 time=148ms TTL=43\n',
        '\n', 'Ping statistics for 173.194.24.138:\n', '
        Packets: Sent = 5, Received = 5, Lost = 0 (0% loss),\n',
        'Approximate round trip times in milli-seconds:\n', '
        Minimum = 148ms, Maximum = 149ms, Average = 148ms\n']

"""

from __future__ import with_statement
import os
import re
import platform

import pytomo.config_pytomo as config_pytomo

RTT_PATTERN_LINUX = (
    r"rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/\d+.\d+ ms")
RTT_PATTERN_WINDOWS = (
    r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms")

RTT_MATCH_WINDOWS = "Minimum = "
RTT_MATCH_LINUX = "rtt min/avg/max/mdev = "

def ping_ip(ip_address, ping_packets=config_pytomo.PING_PACKETS):
    "Return a list of the min, avg, max and mdev ping values"
    current_system = platform.system()
    if current_system == 'Linux':
        ping_option_nb_pkts = '-c %d' % ping_packets
        rtt_match = RTT_MATCH_LINUX
        rtt_pattern = RTT_PATTERN_LINUX
    elif (current_system == 'Microsoft' or current_system == 'Windows'):
        ping_option_nb_pkts = '-n %d' % ping_packets
        rtt_match = RTT_MATCH_WINDOWS
        rtt_pattern = RTT_PATTERN_WINDOWS
    else:
        config_pytomo.LOG.warn("Ping option is not known on your system")
        ping_option_nb_pkts = ''
    my_cmd = 'ping %s %s' % (ping_option_nb_pkts, ip_address)
    ping_result = os.popen(my_cmd)
    rtt_stats = None
    # instead of grep which is less portable
    for rtt_line in ping_result:
        if rtt_match in rtt_line:
            rtt_stats = rtt_line.strip()
            break
    if not rtt_stats:
        config_pytomo.LOG.info("No RTT stats found")
        return None
    rtt_times = re.search(rtt_pattern, rtt_stats)
    if rtt_times:
        rtt_values = rtt_times.groups()
        config_pytomo.LOG.debug(
            "RTT stats found for ip: %s" % ip_address)
        return map(float, rtt_values)
    config_pytomo.LOG.error(
        "The ping returned an unexpected RTT fomat: %s" % rtt_times)
    return None

