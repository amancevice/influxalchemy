# InfluxAlchemy

[![pytest](https://github.com/amancevice/influxalchemy/workflows/pytest/badge.svg)](https://github.com/amancevice/influxalchemy/actions)
[![PyPI Version](https://badge.fury.io/py/influxalchemy.svg)](https://badge.fury.io/py/influxalchemy)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fd0e15a31b2ed8a0ccca/test_coverage)](https://codeclimate.com/github/amancevice/influxalchemy/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/fd0e15a31b2ed8a0ccca/maintainability)](https://codeclimate.com/github/amancevice/influxalchemy/maintainability)

Query InfluxDB using SQLAlchemy-style syntax


## Installation

```bash
pip install influxalchemy
```


## Usage

```python
import influxdb
import influxalchemy
```


### Define InfluxAlchemy Measurements

```python
class Widgets(influxalchemy.Measurement):
    __measurement__ = 'widgets'


class Wombats(influxalchemy.Measurement):
    __measurement__ = 'wombats'
```

The class-attribute `__measurement__` can be omitted and will default to the class name if absent.


### Open InfluxAlchemy Connection


```python
db = influxdb.DataFrameClient(database="example")
flux = influxalchemy.InfluxAlchemy(db)
```


## Query InfluxDB


### Query Single Measurement

```python
# SELECT * FROM widgets;
flux.query(Widgets)
```


### Query Ad Hoc Measurement

```python
# SELECT * from /.*/;
flux.query(influxalchemy.Measurement.new("/.*/"))
```


### Select Fields of Measurement

```python
# SELECT tag1, field2 FROM widgets;
flux.query(Widgets.tag1, Widgets.field2)
```


### Query Across Measurements

```python
# SELECT * FROM /widgets|wombats/;
flux.query(Widgets | Wombats)
```


### Filter Tags

```python
# SELECT * FROM widgets WHERE tag1 = 'fizz';
flux.query(Widgets).filter(Widgets.tag1 == "fizz")
```


### Filter Tags with 'like'

```python
# SELECT * FROM widgets WHERE tag1 =~ /z$/;
flux.query(Widgets).filter(Widgets.tag1.like("/z$/"))
```


### Chain Filters

```python
clause1 = Widgets.tag1 == "fizz"
clause2 = Widgets.tag2 == "buzz"

# SELECT * FROM widgets WHERE tag1 = 'fizz' AND tag2 = 'buzz';
flux.query(Widgets).filter(clause1 & clause2)

# SELECT * FROM widgets WHERE tag1 = 'fizz' OR tag2 = 'buzz';
flux.query(Widgets).filter(clause1 | clause2)
```


### Group By

```python
# SELECT * FROM widgets GROUP BY time(1d);
flux.query(Widgets).group_by("time(1d)")

# SELECT * FROM widgets GROUP BY tag1;
flux.query(Widgets).group_by(Widgets.tag1)
```


### Time

```python
# SELECT * FROM widgets WHERE (time > now() - 7d);
flux.query(Widgets).filter(Widgets.time > "now() - 7d")

# SELECT * FROM widgets WHERE time >= '2016-01-01' AND time <= now() - 7d;
d = date(2016, 1, 1)
flux.query(Widgets).filter(Widgets.time.between(d, "now() - 7d"))
```

Note that naive datetime object will be assumed in UTC timezone.
