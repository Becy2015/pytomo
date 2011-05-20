#!/usr/bin/env python
"""
    Mock_test module for the lib_youtube_api
"""
from __future__ import absolute_import

import nose.tools as ntools
from ..pytomo import lib_youtube_api
from ..pytomo import lib_cache_url
from ..pytomo import start_pytomo

import doctest
doctest.testmod(start_pytomo)


SAMPLE_WEBPAGE_1 = set( [ '/watch?v=Kav0FEhtLug',
                         '/videos?feature=mh',
                         'http://upload.youtube.com/my_videos_upload',
                         '/signup?next=%2Fcharts',
                         '/charts?&opt_out_ackd=1hl=fr&persist_hl=1',
                         '/videos?s=mp',
                         '/watch?v=Kav0FEhtLug',
                         '/user/lifesforsharing',
                         '/watch?v=S-6S2cTp8Pw',
                         '/watch?v=S-6S2cTp8Pw',
                         '/user/abidjannetTV',
                         '/watch?v=xAWEeR4N22s',
                         '/watch?v=xAWEeR4N22s',
                         '/watch?v=JqjJPSP_UHg',
                         '/watch?v=ccNQL-ObZso',
                         '/watch?v=tlMZ_rCUST4',
                         '/watch?v=7maa7HkQ__E',
                         '/watch?v=Cqak99E5OY0',
                         '/watch?v=wQtY0mMPlq4',
                         '/watch?v=Ll0nwo_0x-w',
                         '/watch?v=2hPmPKAtZ_E',
                         '/watch?v=WfjcWQxv0eY',
                         '/watch?v=fzwGm0dqYPU',
                         '/watch?v=eTHNBZ2QbNA',
                         '/watch?v=EqWQUptsy9U',
                         '/watch?v=biPbhEqB4-4',
                         '/watch?v=_ALMP_sfQgU',
                         '/watch?v=6UrivgQVEl8',
                         '/watch?v=Liie0TAEQlg',
                         '/watch?v=GPkJxkRhYl4',
                         '/watch?v=M8rmOoqs3sE',
                         '/watch?v=LbCXKMPmBZQ',
                        ])

SAMPLE_WEBPAGE_2 = set ([ '/results?search_query=khan&search=tag',
                 '/results?search_query=harbhajan&search=tag',
                 '/results?search_query=munaf&search=tag',
                 '/results?search_query=patel&search=tag',
                 '/results?search_query=yusuf&search=tag',
                 '/results?search_query=pathan&search=tag',
                 '/results?search_query=suresh&search=tag',
                 '/results?search_query=raina&search=tag',
                 '/results?search_query=ashwin&search=tag',
                 '/results?search_query=ravichandran&search=tag',
                 '/results?search_query=ashish&search=tag',
                 '/results?search_query=nehra&search=tag',
                 '/results?search_query=mahender&search=tag',
                 '/results?search_query=afridi&search=tag',
                 '/results?search_query=sangakara&search=tag',
                 '/results?search_query=kumar&search=tag',
                 '/results?search_query=malinga&search=tag',
                 '/results?search_query=congress&search=tag',
                 '/results?search_query=party&search=tag',
                 '/results?search_query=corruption&search=tag',
                  '/comment_search?username=jevres342',
                  '/user/flow14pari',
                  '/user/jevres342',
                  '/user/maybellwatson',
                  '/user/maybellwatson',
                  '/user/maybellwatson',
                  '/user/warriorphilander',
                  '/user/pakhtoon906',])



EXPECTED_RESULT = set(['http://www.youtube.com/watch?v=6UrivgQVEl8',
                     'http://www.youtube.com/watch?v=_ALMP_sfQgU',
                     'http://www.youtube.com/watch?v=Liie0TAEQlg',
                     'http://www.youtube.com/watch?v=2hPmPKAtZ_E',
                     'http://www.youtube.com/watch?v=EqWQUptsy9U',
                     'http://www.youtube.com/watch?v=S-6S2cTp8Pw',
                     'http://www.youtube.com/watch?v=ccNQL-ObZso',
                     'http://www.youtube.com/watch?v=eTHNBZ2QbNA',
                     'http://www.youtube.com/watch?v=tlMZ_rCUST4',
                     'http://www.youtube.com/watch?v=Cqak99E5OY0',
                     'http://www.youtube.com/watch?v=7maa7HkQ__E',
                     'http://www.youtube.com/watch?v=JqjJPSP_UHg',
                     'http://www.youtube.com/watch?v=biPbhEqB4-4',
                     'http://www.youtube.com/watch?v=Ll0nwo_0x-w',
                     'http://www.youtube.com/watch?v=WfjcWQxv0eY',
                     'http://www.youtube.com/watch?v=LbCXKMPmBZQ',
                     'http://www.youtube.com/watch?v=Kav0FEhtLug',
                     'http://www.youtube.com/watch?v=fzwGm0dqYPU',
                     'http://www.youtube.com/watch?v=M8rmOoqs3sE',
                     'http://www.youtube.com/watch?v=wQtY0mMPlq4',
                     'http://www.youtube.com/watch?v=GPkJxkRhYl4',
                     'http://www.youtube.com/watch?v=xAWEeR4N22s'])



def patch_get_popular_links_1():
    "Function to patch the namespace of the functions to be replaced"
    start_pytomo.configure_log_file('mock_file')
    lib_cache_url._get_all_links = (lib_cache_url.get_all_links)
    lib_cache_url.get_all_links =  lambda x : SAMPLE_WEBPAGE_1

def unpatch_get_popular_links():
    "Function to clear the namespace used for the mock"
    lib_cache_url.get_all_links = lib_cache_url._get_all_links
    delattr(lib_cache_url, '_get_all_links')

@ntools.with_setup(patch_get_popular_links_1, unpatch_get_popular_links)
def test_lib_youtube_api_1():
    "Test fucntion with a webpage with youtube_links"
    links = lib_youtube_api.get_popular_links('week', 25)
    ntools.assert_equals(links, EXPECTED_RESULT)

def patch_get_popular_links_2():
    "Function to patch the namespace of the functions to be replaced"
    start_pytomo.configure_log_file('mock_file')
    lib_cache_url._get_all_links = (lib_cache_url.get_all_links)
    lib_cache_url.get_all_links =  lambda x : SAMPLE_WEBPAGE_2

@ntools.with_setup(patch_get_popular_links_2, unpatch_get_popular_links)
def test_lib_youtube_api_2():
    "Test function with a webpage with no youtube links"
    links = lib_youtube_api.get_popular_links('week', 25)
    ntools.assert_equals(links, set([]))







