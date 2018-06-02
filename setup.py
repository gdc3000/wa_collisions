"""
Set up file for python module wa_collisions.

This file supports the installation of the wa_collisions module.
The module allows user to create interactive visualizations and
statistically compare patterns in vehicle collisions in Washington.
Adaped from shablona template.
"""


<<<<<<< HEAD
import os
<<<<<<< HEAD
from setuptools import setup, find_packages
PACKAGES = find_packages()

# Get version and release info, which is all stored in
# vehicle_collisions/version.py
#VER_FILE = os.path.join('wa_collisions/', 'version.py')
#with open(VER_FILE) as f:
#    exec(f.read())
=======
=======
>>>>>>> ddebf317cd4e060c592255de780a799260f15e49
from setuptools import setup
>>>>>>> 340dfdd116364338350e0b2c26047dd4ee07f52d

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

<<<<<<< HEAD
PACKAGES = ['wa_collisions.interactive_plotting',
            'wa_collisions.neighborhood_reader',
            'wa_collisions.read_clean_integrate_data',
            'wa_collisions.render_stats',
            'wa_collisons.visualizer']

# from the requirements.txt
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

OPTS = dict(name='WA Collisions',
=======
PACKAGES = ['wa_collisions']

<<<<<<< HEAD
opts = dict(name='wa_collisions',
>>>>>>> 340dfdd116364338350e0b2c26047dd4ee07f52d
=======
OPTS = dict(name='wa_collisions',
>>>>>>> ddebf317cd4e060c592255de780a799260f15e49
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
<<<<<<< HEAD
            version='1.0',
            packages=PACKAGES,
            package_data='data/*',
            #install_requires=REQUIRES,
            #requires=REQUIRES
            )
=======
            version='==1.0',
            packages=PACKAGES)
>>>>>>> 340dfdd116364338350e0b2c26047dd4ee07f52d


if __name__ == '__main__':
    setup(**OPTS)
