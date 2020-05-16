from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    author='amancevice',
    author_email='smallweirdnum@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Database',
        'Topic :: Utilities',
    ],
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
