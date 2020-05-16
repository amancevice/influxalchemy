from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    author='amancevice',
    author_email='smallweirdnum@gmail.com',
    description='Interact with InfluxDB using SQLAlchemy-style syntax',
    install_requires=[
        'influxdb >= 5.0',
        'pytz >= 2018.3',
        'requests >= 2.20',
        'six >= 1.11',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='influxalchemy',
    packages=find_packages(exclude=['tests']),
    python_requires='>= 3.5',
    setup_requires=['setuptools_scm'],
    url='https://github.com/amancevice/influxalchemy',
    use_scm_version=True,
)
