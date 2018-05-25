"""
Set up file for python module wa_collisions. 

This file supports the installation of the wa_collisions module. 
The module allows user to create interactive visualizations and
statistically compare patterns in vehicle collisions in Washington.
"""


import os
from setuptools import setup, find_packages
PACKAGES = find_packages()

# Get version and release info, which is all stored in
# vehicle_collisions/version.py
VER_FILE = os.path.join('wa_collisions', 'version.py')
with open(VER_FILE) as f:
    exec(f.read())

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
LONG_DESCRIPTION = 'Python module that allows the user to explore accidents'
LONG_DESCRIPTION = LONG_DESCRIPTION + ' around Seattle. The user can create '
LONG_DESCRIPTION = LONG_DESCRIPTION + 'interactive visualizations that'
LONG_DESCRIPTION = LONG_DESCRIPTION + ' compare different collision conditions'
LONG_DESCRIPTION = LONG_DESCRIPTION + ' and their locations around'
LONG_DESCRIPTION = LONG_DESCRIPTION + ' the city.'

PACKAGES = ['wa_collisions.create_indicator_map_visual',
            'wa_collisions.interactive_plotting',
            'wa_collisions.neighborhood_reader',
            'wa_collisions.read_clean_integrate_data',
            'wa_collisions.render_stats',
            'wa_collisions.version',
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
            version='1.0',
            packages=PACKAGES,
            package_data='data/*',
            install_requires=REQUIRES,
            requires=REQUIRES)


if __name__ == '__main__':
    setup(**OPTS)
