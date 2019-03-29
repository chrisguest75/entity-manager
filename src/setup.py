"""Describe the modules so that PyTest tests can find them"""

# this is standard Python packaging from http://python-packaging.readthedocs.io
from setuptools import setup

# as this is for testing purposes only, don't provide metadata
setup(name='entity_manager', version='0.1', packages=['entity_manager'])
