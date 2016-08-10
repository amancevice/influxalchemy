""" InfluxAlchemy Query Tests. """

import influxdb
import mock
from influxalchemy.client import InfluxAlchemy
from influxalchemy.measurement import Measurement
from nose import tools


@mock.patch("influxdb.InfluxDBClient.query")
def test_group_by(mock_qry):
    mock_qry.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("fizz")).group_by("buzz")
    tools.assert_equal(str(query), "SELECT * FROM fizz GROUP BY buzz;")


@mock.patch("influxdb.InfluxDBClient.query")
def test_filter_by(mock_qry):
    mock_qry.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("fizz")).filter_by(buzz="goo")
    tools.assert_equal(str(query), "SELECT * FROM fizz WHERE (buzz = 'goo');")


def test_tags():
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    fizz = Measurement.new("fizz")
    query = client.query(fizz.buzz, fizz.bug)
    tools.assert_equal(str(query), "SELECT buzz, bug FROM fizz;")


@mock.patch("influxalchemy.InfluxAlchemy.tags")
@mock.patch("influxalchemy.InfluxAlchemy.fields")
def test_get_tags_fields(mock_fields, mock_tags):
    mock_tags.return_value = ["fizz", "buzz"]
    mock_fields.return_value = ["foo", "goo"]
    db = influxdb.InfluxDBClient(database="example")
    client = InfluxAlchemy(db)
    fizz = Measurement.new("fuzz")
    query = client.query(fizz)
    tools.assert_equal(str(query), "SELECT fizz, buzz, foo, goo FROM fuzz;")
