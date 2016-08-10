""" InfluxAlchemy Client. """

from . import query
from . import measurement


class InfluxAlchemy(object):
    def __init__(self, client):
        self.bind = client
        assert self.bind._database is not None, \
            "InfluxDB client database cannot be None"

    def query(self, *entities):
        return query.InfluxDBQuery(entities, self)

    def measurements(self):
        results = self.bind.query("SHOW MEASUREMENTS;")
        for res in results.get_points():
            yield measurement.Measurement.new(str(res["name"]))

    def tags(self, measurement):
        tags = self.bind.query("SHOW tag keys FROM %s" % measurement)
        pts = sorted(set(y for x in tags.get_points() for y in x.values()))
        return pts

    def fields(self, measurement):
        fields = self.bind.query("SHOW field keys FROM %s" % measurement)
        pts = sorted(set(y for x in fields.get_points() for y in x.values()))
        return pts
