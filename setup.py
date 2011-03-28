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

from distutils.core import setup

VERSION = "0.1.0"

LICENSE = "GPLv2"

KWARGS = {
    'name': "Pytomo",
    'version': VERSION,
    'description': "Python tomography tool",
    'author': "Louis Plissonneau",
    'author_email': "louis.plissonneau@gmail.com",
    'url': "http://code.google.com/p/pytomo",
    'packages': ['pytomo','pytomo/dns', 'pytomo/dns/rdtypes',
                 'pytomo/dns/rdtypes/ANY', 'pytomo/dns/rdtypes/IN',
                 'pytomo/kaa_metadata', 'pytomo/kaa_metadata/audio',
                 'pytomo/kaa_metadata/disc', 'pytomo/kaa_metadata/image',
                 'pytomo/kaa_metadata/video', 'pytomo/kaa_metadata/games',
                 'pytomo/kaa_metadata/misc'],
    'scripts': ["bin/pytomo"],
    'long_description': open('README.txt').read(),
    'platforms': ["Linux", "Windows"],
    'license': LICENSE,
}

setup(**KWARGS)
