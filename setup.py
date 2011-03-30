#!/usr/bin/env python
"""Module to distribute the code with distutils

For running Pyinstaller, use:
# **From Pytomo sources directory**
find . -name '*.pyc' -delete
rm -r build
# **From Pyinstaller repository**
python2.5 Makespec.py --onefile \
    -p ~/streaming/pytomo/Pytomo/ -p ~/streaming/pytomo/Pytomo/pytomo/ \
    -o ~/streaming/pytomo/Pytomo/ \
    ~/streaming/pytomo/Pytomo/bin/pytomo
# Check differences
diff  ~/streaming/pytomo/Pytomo/pytomo_named.spec \
        ~/streaming/pytomo/Pytomo/pytomo.spec
# Run with automatic naming of exe
python2.5 Build.py ~/streaming/pytomo/Pytomo/pytomo_named.spec

"""

import distutils.core

distutils.core.USAGE = """NO SETUP IS NEEDED TO LAUNCH THE PROGRAM.

This setup is only used to generate the source distribution: './setup.py sdist'
[other setup commands are described in './setup.py --help']

Use './start_crawl.py' to start the crawl.
You can check the options with 'start_crawl.py -h'.
You can configure options in the command line of start_crawl.py or in the
pytomo/config_pytomo.py file.
"""

VERSION = '0.1.3'

LICENSE = 'GPLv2'

KWARGS = {
    'name': 'Pytomo',
    'version': VERSION,
    'description': 'Python tomography tool',
    'author': 'Louis Plissonneau',
    'author_email': 'louis.plissonneau@gmail.com',
    'url': 'http://code.google.com/p/pytomo',
    'packages': ['pytomo','pytomo/dns', 'pytomo/dns/rdtypes',
                 'pytomo/dns/rdtypes/ANY', 'pytomo/dns/rdtypes/IN',
                 'pytomo/kaa_metadata', 'pytomo/kaa_metadata/audio',
                 'pytomo/kaa_metadata/image', 'pytomo/kaa_metadata/video',
                 'pytomo/kaa_metadata/misc'],
    'scripts': ['bin/pytomo', 'start_crawl.py'],
    'long_description': open('README.txt').read(),
    'platforms': ['Linux', 'Windows', 'Mac'],
    'license': LICENSE,
    'classifiers': ['Development Status :: 4 - Beta',
                    'Environment :: Console',
                    'Intended Audience :: Science/Research',
                    'Operating System :: OS Independent',
                    'Operating System :: POSIX',
                    'Operating System :: Microsoft',
                    'Operating System :: MacOS :: MacOS X',
                    'Programming Language :: Python :: 2',
                    'Topic :: Internet',
                   ],
}


distutils.core.setup(**KWARGS)

