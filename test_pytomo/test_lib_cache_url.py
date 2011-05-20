#!/usr/bin/env python

"""
    Mock test for lib_cache_url

"""
from __future__ import absolute_import
import nose.tools as ntools
from ..pytomo import lib_cache_url
from ..pytomo import start_pytomo
import urllib
import cPickle
import random
start_pytomo.configure_log_file('mock')

import doctest
doctest.testmod(lib_cache_url)

SAMPLE_YOUTUBE_FILE = 'sample_youtube_page.txt'
SAMPLE_RESULT_FILE = 'res.pkl'
SAMPLE_YOUTUBE_LINKS_1 =  set(
    ['http://www.youtube.com/watch?v=ljUx3w_asrg',
     'http://www.youtube.com/watch?v=8PenzwVatVU',
     'http://www.youtube.com/watch?v=L6FwqGgqaWs',
     'http://www.youtube.com/watch?v=mEumN8IqyTY',
     'http://www.youtube.com/watch?v=ZOMKjneriTg',
     'http://www.youtube.com/watch?v=qVaBsIVnxnM',
     'http://www.youtube.com/watch?v=ye6TcoCv51o',
     'http://www.youtube.com/watch?v=XpUbgT6oV_c',
     'http://www.youtube.com/watch?v=wYecrTp_aUE',
     'http://www.youtube.com/watch?v=_85natBOae4',
     'http://www.youtube.com/watch?v=-y4vMlrRBNo',
     'http://www.youtube.com/watch?v=3ysHPt3wp0M',
     'http://www.youtube.com/watch?v=i5Qz2Zfm7-w',
     'http://www.youtube.com/watch?v=T0iwCku8cGo',
     'http://www.youtube.com/watch?v=Iy6gZ1mY1Z4',
     'http://www.youtube.com/watch?v=ELuvTh4Dg58',
     'http://www.youtube.com/watch?v=HSdD_jWE4jc',
     'http://www.youtube.com/watch?v=_eN-cA74n3M',
     'http://www.youtube.com/watch?v=lgv_-X9LPlY',
     'http://www.youtube.com/watch?v=TGoTqhyzYlc'])

SAMPLE_YOUTUBE_LINKS_2 = set(
    ['http://www.youtube.com/watch?v=-HFvUY-VdQM&feature=related',
      'http://www.youtube.com/watch?v=-VNypLbQUv4&feature=related',
      'http://www.youtube.com/watch?v=7q5gZFR2dxs&feature=related',
      'http://www.youtube.com/watch?v=7rZbvi6Tj6E&feature=related',
      'http://www.youtube.com/watch?v=8CVLU5hVgKg&feature=related',
      'http://www.youtube.com/watch?v=CoNtYC_XDC8&feature=related',
      'http://www.youtube.com/watch?v=Fn01zVMX6Q0&feature=related',
      'http://www.youtube.com/watch?v=G1d8-4cwZgM&feature=related',
      'http://www.youtube.com/watch?v=IrRA7WMI1ks&feature=related',
      'http://www.youtube.com/watch?v=IxRksF-F5ds',
      'http://www.youtube.com/watch?v=O6475u0wEG0&feature=related',
      'http://www.youtube.com/watch?v=OFIb7VG-KQ8&feature=related',
      'http://www.youtube.com/watch?v=OdF-oiaICZI&feature=related',
      'http://www.youtube.com/watch?v=RyzTqv5fMsw&feature=related',
      'http://www.youtube.com/watch?v=SKYWOwWAguk&feature=related',
      'http://www.youtube.com/watch?v=g4bBff9aBRw&feature=fvwrel',
      'http://www.youtube.com/watch?v=iG4EaKYHIWM&feature=related',
      'http://www.youtube.com/watch?v=nCwpeyM_FGs&feature=related',
      'http://www.youtube.com/watch?v=rvEjdQv1Ftk&feature=related',
      'http://www.youtube.com/watch?v=s9SpX64g84U&feature=related',
      'http://www.youtube.com/watch?v=w3PX267adKs&feature=related',
      'http://www.youtube.com/watch?v=y2kEx5BLoC4&feature=list_related& \
       playnext=1&list=MLGxdCwVVULXfxx-61LMYHbwpcwAvZd-rI',
      'http://www.youtube.com/watch?v=y2kEx5BLoC4&feature=related'])

# Test for the get_all_links function
def patch_get_all_links():
    "Function to patch the namespace of the functions to be replaced"
    urllib._urlopen = urllib.urlopen
    sample_webpage = open(SAMPLE_YOUTUBE_FILE, 'r')
    urllib.urlopen = lambda x, proxies = None: sample_webpage

def unpatch_get_all_links():
    "Function to clear the namespace"
    urllib.urlopen = urllib._urlopen
    delattr(urllib, '_urlopen')

@ntools.with_setup(patch_get_all_links, unpatch_get_all_links)
def test_get_all_links():
    "Test fucntion with a webpage with youtube_links"
    url = 'http://www.youtube.com/watch?v=cv5bF2FJQBc'
    links = lib_cache_url.get_all_links(url)
    with open (SAMPLE_RESULT_FILE, 'r') as sample_webpage:
        expected_result = cPickle.load(sample_webpage)
        ntools.assert_equals(links, expected_result)

#Test for get_youtube_links
def patch_get_youtube_links():
    "Function to patch the namespace of the functions to be replaced"
    lib_cache_url._get_all_links = lib_cache_url.get_all_links
    with open(SAMPLE_RESULT_FILE, 'r') as res_pkl:
        links = cPickle.load(res_pkl)
    lib_cache_url.get_all_links = lambda x: links

def unpatch_get_youtube_links():
    "Function to clear the namespace"
    lib_cache_url.get_all_links = lib_cache_url._get_all_links
    delattr(lib_cache_url, '_get_all_links')

@ntools.with_setup(patch_get_youtube_links, unpatch_get_youtube_links)
def test_get_youtube_links():
    "Test fucntion with a webpage with youtube_links"
    url = 'http://www.youtube.com/watch?v=cv5bF2FJQBc'
    max_per_page = 25
    links = lib_cache_url.get_youtube_links(url, 25)
    ntools.assert_equals(links, SAMPLE_YOUTUBE_LINKS_1)


#Test for get_related_urls
def patch_get_related_urls():
    "Function to patch the namespace of the functions to be replaced"
    lib_cache_url._get_links = lib_cache_url.get_links
    lib_cache_url.get_links = lambda x, y, z: SAMPLE_YOUTUBE_LINKS_1

def unpatch_get_related_urls():
    "Function to clear the namespace"
    lib_cache_url.get_links = lib_cache_url._get_links
    delattr(lib_cache_url, '_get_links')

@ntools.with_setup(patch_get_related_urls, unpatch_get_related_urls)
def test_get_related_urls():
    "Test fucntion for get_related_urls"
    url = 'http://www.youtube.com/watch?v=cv5bF2FJQBc'
    max_per_page = 25
    max_per_url = 10
    links = lib_cache_url.get_related_urls(url, max_per_page, max_per_url)
    ntools.assert_true(set(links).issubset(SAMPLE_YOUTUBE_LINKS_1))
    ntools.assert_true(len(links) < 11)

#Test for get_next_round_urls
def mock_trunk_url(url):
    "Function to return the required part of the url"
    return url.split('&', 1)[0]

def mock_get_related_urls(url, max_per_page, max_per_url):
    "Returns the related urls"
    input_links = ['http://www.youtube.com/watch?v=cv5bF2FJQBc',
                      'http://www.youtube.com/watch?v=OdF-oiaICZI']
    if url == input_links[0]:
        selected_links = map(mock_trunk_url,
                         random.sample(SAMPLE_YOUTUBE_LINKS_1,
                                min(max_per_url,
                                    len(SAMPLE_YOUTUBE_LINKS_1
                                       ))))
    elif url == input_links[1]:
        selected_links = map(mock_trunk_url,
                         random.sample(SAMPLE_YOUTUBE_LINKS_2,
                                min(max_per_url,
                                    len(SAMPLE_YOUTUBE_LINKS_2))))
    else:
        selected_links = None
    return selected_links


def patch_get_next_round_urls():
    "Function to patch the namespace of the functions to be replaced"
    lib_cache_url._get_related_urls = lib_cache_url.get_related_urls
    lib_cache_url.get_related_urls = mock_get_related_urls

def unpatch_get_next_round_urls():
    "Function to clear the namespace"
    lib_cache_url.get_related_urls = lib_cache_url._get_related_urls
    delattr(lib_cache_url, '_get_related_urls')

@ntools.with_setup(patch_get_next_round_urls, unpatch_get_next_round_urls)
def test_get_next_round_urls():
    "Test function for get_next_round_urls"
    input_links = ['http://www.youtube.com/watch?v=cv5bF2FJQBc',
                   'http://www.youtube.com/watch?v=OdF-oiaICZI']
    max_per_page = 20
    max_per_url = 5
    related_links = lib_cache_url.get_next_round_urls(input_links,
                                        max_per_page, max_per_url)
    result_set = SAMPLE_YOUTUBE_LINKS_1.union(SAMPLE_YOUTUBE_LINKS_2)
    result_list = map(mock_trunk_url, list(result_set))
    ntools.assert_true(set(related_links).issubset(set(result_list)))
