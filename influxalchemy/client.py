""" InfluxAlchemy Client. """

from . import query
from .measurement import Measurement


class InfluxAlchemy(object):
    """ InfluxAlchemy database session.

        client (InfluxDBClient):  Connection to InfluxDB database
    """
    def __init__(self, client):
        self.bind = client
        # pylint: disable=protected-access
        assert self.bind._database is not None, \
            "InfluxDB client database cannot be None"

    def query(self, *entities):
        """ Query InfluxDB entities. Entities are either Measurements or
            Tags/Fields.
        """
        return query.InfluxDBQuery(entities, self)

    def measurements(self):
        """ Get measurements of an InfluxDB. """
        results = self.bind.query("SHOW MEASUREMENTS;")
        for res in results.get_points():
            yield Measurement.new(str(res["name"]))

    def tags(self, measurement):
        """ Get tags of a measurements in InfluxDB. """
        tags = self.bind.query("SHOW tag keys FROM %s" % measurement)
        pts = sorted(set(y for x in tags.get_points() for y in x.values()))
        return pts

    def fields(self, measurement):
        """ Get fields of a measurements in InfluxDB. """
        fields = self.bind.query("SHOW field keys FROM %s" % measurement)
        pts = sorted(set(y for x in fields.get_points() for y in x.values()))
        return pts
