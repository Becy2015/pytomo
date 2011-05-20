#!/usr/bin/env python
"""Function to get the most popular Youtube videos according to the time frame.
    Arguments:
        time = 'today' or 'month' or 'week' or all_time'
        max_results : In multiples of 25
    Returns: A list containing the list of videos.

   Usage: To use the functions provided in this module independently,
        first place yourself just above pytomo folder.Then:

        import pytomo.start_pytomo
        TIMESTAMP = 'test_timestamp'
        start_pytomo.configure_log_file(TIMESTAMP)

        import pytomo.lib_youtube_api as lib_youtube_api
        time = 'today' # choose from 'today' or 'month' or 'week' or all_time'
        max_results = 25
        time_frame = lib_youtube_api.get_time_frame(time)
        lib_youtube_api.get_popular_links(time_frame, max_results)

"""

from __future__ import absolute_import

from . import lib_cache_url
from . import config_pytomo

# Youtube webpage limitation
MAX_VIDEO_PER_PAGE = 25

def get_time_frame(time=config_pytomo.TIME_FRAME):
    """ Returns the time frame in the form accepted by youtube_api
    >>> from . import start_pytomo
    >>> start_pytomo.configure_log_file('doc_test') #doctest: +ELLIPSIS
    Configuring log file
    Logs are there: ...
    True
    >>> get_time_frame('today')
    't'
    >>> get_time_frame('week')
    'w'
    >>> get_time_frame('month')
    'm'
    >>> get_time_frame('all_time')
    'a'
    >>> get_time_frame('other')
    'a'
    """

    if time == 'today':
        time_frame = 't'
    elif time == 'week':
        time_frame = 'w'
    elif time == 'month':
        time_frame = 'm'
    elif time == 'all_time':
        time_frame = 'a'
    else:
        config_pytomo.LOG.info('Time frame not recognised. '
                               'Assuming All time Popular videos.')
        time_frame = 'a'
    return time_frame

def get_popular_links(time=config_pytomo.TIME_FRAME,
                      max_results=config_pytomo.MAX_PER_PAGE):
    """Returns the most popular youtube links (world-wide).
    The number of videos returned is given as Total_pages.
    (The results returned are in no particular order).
    A set of only Youtube links from url
    """
    config_pytomo.LOG.debug('Getting popular links')
    time_frame = get_time_frame(time)
    if max_results > MAX_VIDEO_PER_PAGE:
        pages = int(max_results) / MAX_VIDEO_PER_PAGE
    else:
        pages = 1
    for page in xrange(pages):
        url = ''.join(
            ('http://www.youtube.com/charts/videos_views?p=2&gl=US&t=',
             time_frame, '&p=', str(page + 1))
                     )
        links = lib_cache_url.get_all_links(url)
        if not links:
            config_pytomo.LOG.warning('No popular link was found')
        popular_links = set()
        for link in links:
            if link.find("/watch") >= 0:
                if link.startswith('/'):
                    link = ''.join(("http://www.youtube.com", link))
                popular_links.add(link)
                if len(popular_links) >= max_results:
                    break
    return popular_links

if __name__ == '__main__':
    import doctest
    doctest.testmod()
