"""
Set up file for python module wa_collisions. 

This file supports the installation of the wa_collisions module. 
The module allows user to create interactive visualizations and
statistically compare patterns in vehicle collisions in Washington.
Adaped from shablona template. 
"""


import os
from setuptools import setup

# used format from https://docs.python.org/2/distutils/setupscript.html

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

PACKAGES = ['wa_collisions']

opts = dict(name='wa_collisions',
            maintainer='Libby Montague, Fei Wang, Geoff Coyner, Salik Warsi',
            maintainer_email='',
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url='https://github.com/gdc3000/wa_collisions',
            download_url='https://github.com/gdc3000/wa_collisions.git',
            license='MIT License',
            classifiers=CLASSIFIERS,
            author='Libby Montague, Fei Wang, Geoff Coyner, Salik Warsi',
            author_email='',
            platforms='Microsoft Windows',
            version='==1.0',
            packages=PACKAGES)


if __name__ == '__main__':
    setup(**opts)
