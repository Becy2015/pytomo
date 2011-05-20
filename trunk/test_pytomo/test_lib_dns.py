#!/usr/bin/env python
"""
    Mock test module for get_ip_addresses

"""
import nose.tools as ntools
from ..pytomo import lib_dns
from ..pytomo.dns import resolver as dns_resolver
from ..pytomo.dns import exception as dns_exception
from ..pytomo import start_pytomo

import doctest
doctest.testmod(lib_dns)

# Mock test for get_ip_addresses
def patch_get_ip_addresses():
    "Function to path the dependent modules of get_ip_addresses"
    start_pytomo.configure_log_file('mock')
    class FakeAddress():
        "Fake IP address class"
        address = '127.0.0.1'
    fake_rdatas = []
    fake_rdatas.append(FakeAddress)
    dns_resolver.Resolver._query = dns_resolver.Resolver.query
    dns_resolver.Resolver.query = lambda x, y : fake_rdatas
    lib_dns._get_default_name_servers  = lib_dns.get_default_name_servers
    lib_dns.get_default_name_servers = lambda : '10.10.10.10'

def unpatch_get_ip_addresses():
    "Function to clear the namespace of the patch"
    dns_resolver.Resolver.query = dns_resolver.Resolver._query
    delattr(dns_resolver.Resolver, '_query')
    lib_dns.get_default_name_servers  = lib_dns._get_default_name_servers
@ntools.with_setup(patch_get_ip_addresses, unpatch_get_ip_addresses)
def test_get_ip_addresses():
    "The test module for get_ip_addresses"
    res = lib_dns.get_ip_addresses('url')
    expected_res = [('127.0.0.1', 'default_10.10.10.10')]
    ntools.assert_equals(res, expected_res)


# Mock test for get_ip_addresses with timeout
def calltimeout():
    "Function to raise Timeout Exception"
    raise dns_exception.Timeout

def patch_get_ip_addresses_timeout():
    "Function to path the dependent modules of get_ip_addresses"
    start_pytomo.configure_log_file('mock')
    class FakeAddress():
        "Fake IP address class"
        address = '127.0.0.1'
    fake_rdatas = []
    fake_rdatas.append(FakeAddress)
    dns_resolver.Resolver._query = dns_resolver.Resolver.query
    # Force timeout
    dns_resolver.Resolver.query = lambda x, y: calltimeout()
    lib_dns._get_default_name_servers  = lib_dns.get_default_name_servers
    lib_dns.get_default_name_servers = lambda : '10.10.10.10'

#@ntools.raises(Exception)
@ntools.with_setup(patch_get_ip_addresses_timeout, unpatch_get_ip_addresses)
def test_get_ip_addresses_timeout():
    "The test module for get_ip_addresses when Timeout occurs"
    lib_dns.get_ip_addresses('url')


# Mock test for get_ip_addresses with DNSException
def patch_get_ip_addresses_dnsexception():
    "Function to path the dependent modules of get_ip_addresses"
    start_pytomo.configure_log_file('mock')
    class FakeAddress():
        "Fake IP address class"
        address = '127.0.0.1'
    fake_rdatas = []
    fake_rdatas.append(FakeAddress)
    dns_resolver.Resolver._query = dns_resolver.Resolver.query
    # Force DNSException
    dns_resolver.Resolver.query = lambda x, y: calldnsexception()
    lib_dns._get_default_name_servers  = lib_dns.get_default_name_servers
    lib_dns.get_default_name_servers = lambda : '10.10.10.10'

def calldnsexception():
    "Function to raise DNSException"
    raise dns_exception.DNSException

#@ntools.raises(dns_exception.DNSException)
@ntools.with_setup(patch_get_ip_addresses_dnsexception, unpatch_get_ip_addresses)
def test_get_ip_addresses_dnsexception():
    "The test module for get_ip_addresses when DNSException occurs"
    lib_dns.get_ip_addresses('url')


