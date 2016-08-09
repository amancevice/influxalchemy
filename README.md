# influxalchemy

Query InfluxDB using SQLAlchemy-style syntax


```python
import influxdb
import influxalchemy
```

## Define InfluxAlchemy Measurements


```python
class Widgets(influxalchemy.Measurement):
    __measurement__ = 'widgets'


class Wombats(influxalchemy.Measurement):
    __measurement__ = 'wombats'
```

## Open InfluxAlchemy Connection


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
