""" InfluxAlchemy client tests. """

import mock
import influxdb
from influxalchemy.client import InfluxAlchemy
from influxalchemy.measurement import Measurement
from influxalchemy.query import InfluxDBQuery
from nose import tools


@mock.patch("influxdb.InfluxDBClient")
def test_query(mock_flux):
    db = influxdb.InfluxDBClient(database="fizz")
    db.query.side_effect = influxdb.exceptions.InfluxDBClientError(None)
    client = InfluxAlchemy(db)
    query = client.query(Measurement.new("buzz"))
    tools.assert_equal(str(query), "SELECT * FROM buzz;")


@mock.patch("influxdb.InfluxDBClient.query")
def test_measurements(mock_flux):
    mock_res = mock.MagicMock()
    mock_res.get_points.return_value = [{"name": "fizz"}]
    mock_flux.return_value = mock_res
    db = influxdb.InfluxDBClient(database="fizz")
    client = InfluxAlchemy(db)
    measurements = list(client.measurements())
    mock_flux.assert_called_once_with("SHOW MEASUREMENTS;")
