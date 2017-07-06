import os
from setuptools import setup

thisdir = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(thisdir, 'requirements.txt')) as f:
    requirements = list(filter(
        lambda x: not not x,
        f.read().splitlines()
    ))


setup(
    name='spotify-api',
    version='0.0.2',
    description='Python client for the Spotify web API',
    author='Steinthor Palsson',
    author_email='steini90@gmail.com',
    url='https://github.com/steinitzu/spotify-api',
    license='MIT',
    install_requires=requirements,
    packages=['spotify']
)
