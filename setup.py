import textwrap
from setuptools import setup

setup(
    author='amancevice',
    author_email='smallweirdnum@gmail.com',
    description='Interact with InfluxDB using SQLAlchemy-style syntax',
    install_requires=[
        'influxdb >= 5.0.0',
        'pytz >= 2018.3',
        'requests >= 2.20.0',
        'six >= 1.11.0',
    ],
    name='influxalchemy',
    packages=['influxalchemy'],
    setup_requires=['setuptools_scm'],
    url='https://github.com/amancevice/influxalchemy',
    use_scm_version=True,
)
