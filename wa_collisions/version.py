"""
Version file for wa_collisions. 
Adapted from shablona template.
"""

__version__ = "1.0"
from __future__ import absolute_import, division, print_function
from os.path import join as pjoin


# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases


# Construct full version string from these.

_ver = [_version_major, _version_minor]

if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = [
    'Development Status :: Version 1',
    'Environment :: Jupyter Notebook',
    'Intended Audience :: Data Scientists',
    'License :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Topic :: Collisions in Seattle',
    'Topic :: Neighborhood Visualizations'
    ]

DESCRIPTION = 'Understanding collision patterns in Seattle'
LONG_DESCRIPTION = """

wa_collisions

========

wa_collisions is a module that allows users to create interactive
visualizations in python of vehicle collisions in Seattle. 

There are example jupyter notebooks for implementation in the github
repository. 

Please visit the readme for more information README_.

.. _README: https://github.com/gdc3000/wa_collisions/blob/master/README.md

License

=======

``wa_collisions`` is licensed under the terms of the MIT license. See the file
"LICENSE" for information on the history of this software, terms & conditions
for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2018, Libby Montague, Fei Wang, Geoff Coyner, Salik Warsi.

"""

NAME = "WA Collisions"
MAINTAINER = "Libby Montague, Fei Wang, Geoff Coyner, Salik Warsi"
MAINTAINER_EMAIL = ""
DESCRIPTION = DESCRIPTION
LONG_DESCRIPTION = LONG_DESCRIPTION
URL = "https://github.com/gdc3000/wa_collisions"
DOWNLOAD_URL = "https://github.com/gdc3000/wa_collisions.git"
LICENSE = "MIT"
AUTHOR = "Libby Montague, Fei Wang, Geoff Coyner, Salik Warsi"
AUTHOR_EMAIL = ""
PLATFORMS = "Microsoft Windows"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGE_DATA = 'data/*'
REQUIRES = ['branca==0.3.0',
            'certifi==2018.4.16',
            'chardet==3.0.4',
            'click==6.7',
            'click-plugins==1.0.3',
            'cligj==0.4.0',
            'cycler==0.10.0',
            'descartes==1.1.0',
            'Fiona==1.7.11.post2',
            'folium==0.5.0',
            'geopandas==0.3.0',
            'idna==2.6',
            'Jinja2==2.10',
            'kiwisolver==1.0.1',
            'MarkupSafe==1.0',
            'matplotlib==2.2.2',
            'munch==2.3.2',
            'numpy==1.14.3',
            'pandas==0.23.0',
            'pyparsing==2.2.0',
            'pyproj==1.9.5.1',
            'python-dateutil==2.7.3',
            'pytz==2018.4',
            'requests==2.18.4',
            'Shapely==1.6.4.post1',
            'six==1.11.0',
            'urllib3==1.22'
           ]