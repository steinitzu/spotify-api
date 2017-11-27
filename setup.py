import os
from setuptools import setup

thisdir = os.path.realpath(os.path.dirname(__file__))

setup(
    name='spotify-api',
    version='0.0.8',
    description='Python client for the Spotify web API',
    author='Steinthor Palsson',
    author_email='steini90@gmail.com',
    url='https://github.com/steinitzu/spotify-api',
    license='MIT',
    install_requires=['requests>=2.18.1'],
    packages=['spotify']
)
