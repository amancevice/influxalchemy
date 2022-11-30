"""
InfluxAlchemy Client.
"""
from influxalchemy import query
from influxalchemy.measurement import Measurement


class InfluxAlchemy:
    """
    InfluxAlchemy database session.

    client (InfluxDBClient):  Connection to InfluxDB database
    """

    def __init__(self, client):
        self.bind = client
        # pylint: disable=protected-access
        assert (
            self.bind._database is not None
        ), "InfluxDB client database cannot be None"

    def query(self, *entities):
        """
        Query InfluxDB entities. Entities are either Measurements or
        Tags/Fields.
        """
        return query.InfluxDBQuery(entities, self)

    def measurements(self):
        """
        Get measurements of an InfluxDB.
        """
        results = self.bind.query("SHOW MEASUREMENTS;")
        for res in results.get_points():
            yield Measurement.new(str(res["name"]))

    def tags(self, measurement):
        """
        Get tags of a measurements in InfluxDB.
        """
        tags = self.bind.query("SHOW tag keys FROM %s" % measurement)
        pts = sorted(set(t["tagKey"] for t in tags.get_points()))
        return pts

    def fields(self, measurement):
        """
        Get fields of a measurements in InfluxDB.
        """
        fields = self.bind.query("SHOW field keys FROM %s" % measurement)
        pts = sorted(set(f["fieldKey"] for f in fields.get_points()))
        return pts
