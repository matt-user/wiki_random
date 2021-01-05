'''
Wiki Rand python package configuration.

Matt Auer <mattauer@umich.edu>
'''

from setuptools import setup

setup(
    name='wiki_rand',
    verion='0.1.0',
    packages=['wiki_rand'],
    include_package_data=True,
    install_requires=[
        'Flask==1.1.2',
        'requests==2.25.1',
        'pycodestlye==2.6.0',
        'pydocstyle==5.1.1',
        'pyline==2.6.0',
    ],
)