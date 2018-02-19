import textwrap
from setuptools import setup

setup(
    name='influxalchemy',
    version='0.1.1',
    author='amancevice',
    author_email='smallweirdnum@gmail.com',
    packages=['influxalchemy'],
    url="http://www.smallweirdnumber.com",
    description='Interact with InfluxDB using SQLAlchemy-style syntax',
    long_description=textwrap.dedent(
        '''See GitHub_ for documentation.
        .. _GitHub: https://github.com/amancevice/influxalchemy'''),
    install_requires=[
        'pytz>=2016.10',
        'influxdb>=3.0.0',
        'six>=1.11.0'])
