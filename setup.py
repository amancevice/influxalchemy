import os
import re
from setuptools import setup

NAME = "influxalchemy"
AUTHOR = "amancevice"
EMAIL = "smallweirdnum@gmail.com"
DESC = "Interact with InfluxDB using SQLAlchemy-style syntax"
LONG = """See GitHub_ for documentation.
.. _GitHub: https://github.com/amancevice/influxalchemy"""
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Utilities",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python"]


def version():
    search = r"^__version__ *= *['\"]([0-9.]+)['\"]"
    initpy = open("./influxalchemy/__init__.py").read()
    return re.search(search, initpy, re.MULTILINE).group(1)

setup(
    name=NAME,
    version=version(),
    author=AUTHOR,
    author_email=EMAIL,
    packages=[NAME],
    url="http://www.smallweirdnumber.com",
    description=DESC,
    long_description=LONG,
    classifiers=CLASSIFIERS,
    install_requires=["influxdb>=3.0.0"],
    test_suite="nose.collector")
