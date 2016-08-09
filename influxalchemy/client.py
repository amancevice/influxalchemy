""" InfluxAlchemy Client. """

from . import query
from . import measurement


class InfluxAlchemy(object):
    def __init__(self, client):
        self._client = client
        assert self._client._database is not None, \
            "InfluxDB client database cannot be None"

    def query(self, *entities):
        return query.InfluxDBQuery(entities, self._client)

    def measurements(self):
        results = self._client.query("SHOW MEASUREMENTS;")
        for res in results.get_points():
            yield measurement.Measurement.generate(str(res["name"]))
