""" InfluxAlchemy client tests. """
from unittest import mock

import influxdb
from influxalchemy.client import InfluxAlchemy
from influxalchemy.measurement import Measurement


@mock.patch("influxdb.InfluxDBClient")
def test_query(mock_flux):
    db = influxdb.InfluxDBClient(database="fizz")
    db.query.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("buzz"))
    assert str(query) == "SELECT * FROM buzz;"


@mock.patch("influxdb.InfluxDBClient.query")
def test_measurements(mock_flux):
    mock_res = mock.MagicMock()
    mock_res.get_points.return_value = [{"name": "fizz"}]
    mock_flux.return_value = mock_res
    db = influxdb.InfluxDBClient(database="fizz")
    client = InfluxAlchemy(db)
    list(client.measurements())
    mock_flux.assert_called_once_with("SHOW MEASUREMENTS;")


@mock.patch("influxdb.InfluxDBClient.query")
def test_tags(mock_flux):
    mock_res = mock.MagicMock()
    mock_res.get_points.return_value = [{"tagKey": "sensor_id"}]
    mock_flux.return_value = mock_res
    db = influxdb.InfluxDBClient(database="fizz")
    client = InfluxAlchemy(db)
    assert client.tags(Measurement.new("environment")) == ["sensor_id"]


@mock.patch("influxdb.InfluxDBClient.query")
def test_fields(mock_flux):
    mock_res = mock.MagicMock()
    mock_res.get_points.return_value = [
        {"fieldKey": "humidity", "fieldType": "float"},
        {"fieldKey": "temperature", "fieldType": "float"},
    ]
    mock_flux.return_value = mock_res
    db = influxdb.InfluxDBClient(database="fizz")
    client = InfluxAlchemy(db)
    exp = ["humidity", "temperature"]
    assert client.fields(Measurement.new("environment")) == exp
