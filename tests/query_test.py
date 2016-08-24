""" InfluxAlchemy Query Tests. """

import influxdb
import mock
from influxalchemy.client import InfluxAlchemy
from influxalchemy.measurement import Measurement


@mock.patch("influxdb.InfluxDBClient.query")
def test_repr(mock_qry):
    mock_qry.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("fizz"))
    assert repr(query) == "SELECT * FROM fizz;"


@mock.patch("influxdb.InfluxDBClient.query")
def test_execute(mock_qry):
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("fizz").buzz)
    query.execute()
    mock_qry.assert_called_with("SELECT buzz FROM fizz;")


@mock.patch("influxdb.InfluxDBClient.query")
def test_filter(mock_qry):
    mock_qry.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    meas = Measurement.new("fizz")
    query = client.query(meas).filter(meas.buzz == "goo")
    assert repr(query) == "SELECT * FROM fizz WHERE (buzz = 'goo');"


@mock.patch("influxdb.InfluxDBClient.query")
def test_group_by(mock_qry):
    mock_qry.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("fizz")).group_by("buzz")
    assert str(query) == "SELECT * FROM fizz GROUP BY buzz;"


@mock.patch("influxdb.InfluxDBClient.query")
def test_filter_by(mock_qry):
    mock_qry.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("fizz")).filter_by(buzz="goo")
    assert str(query) == "SELECT * FROM fizz WHERE (buzz = 'goo');"


def test_tags():
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    fizz = Measurement.new("fizz")
    query = client.query(fizz.buzz, fizz.bug)
    assert str(query) == "SELECT buzz, bug FROM fizz;"


@mock.patch("influxalchemy.InfluxAlchemy.tags")
@mock.patch("influxalchemy.InfluxAlchemy.fields")
def test_get_tags_fields(mock_fields, mock_tags):
    mock_tags.return_value = ["fizz", "buzz"]
    mock_fields.return_value = ["foo", "goo"]
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    fizz = Measurement.new("fuzz")
    query = client.query(fizz)
    assert str(query) == "SELECT fizz, buzz, foo, goo FROM fuzz;"
