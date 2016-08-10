""" InfluxDB Query Object. """

import itertools

import influxdb
from . import measurement


class InfluxDBQuery(object):
    def __init__(self, entities, client, expressions=None, groupby=None):
        self._entities = entities
        self._client = client
        self._expressions = expressions or ()
        self._groupby = groupby

    def __str__(self):
        select = ", ".join(self._select)
        from_ = self._from
        where = " AND ".join(self._where)
        if any(where):
            iql = "SELECT %s FROM %s WHERE %s" % (select, from_, where)
        else:
            iql = "SELECT %s FROM %s" % (select, from_)
        if self._groupby is not None:
            iql += " GROUP BY %s" % self._groupby
        return "%s;" % iql

    def __repr__(self):
        return str(self)

    def execute(self):
        return self._client.bind.query(str(self))

    def filter(self, *expressions):
        expressions = self._expressions + expressions
        return InfluxDBQuery(self._entities, self._client, expressions)

    def filter_by(self, **kwargs):
        expressions = self._expressions
        for key, val in kwargs.items():
            expressions += measurement.TagExp.eq(key, val),
        return InfluxDBQuery(self._entities, self._client, *expressions)

    def group_by(self, groupby):
        return InfluxDBQuery(
            self._entities, self._client, self._expressions, groupby)

    @property
    def measurement(self):
        measurements = set(x.measurement for x in self._entities)
        return reduce(lambda x, y: x | y, measurements)

    @property
    def _select(self):
        selects = []
        for ent in self._entities:
            # Entity is a Tag
            if isinstance(ent, measurement.Tag):
                selects.append(str(ent))
            # Entity is a Measurement
            else:
                try:
                    for tag in self._client.tags(ent):
                        selects.append(tag)
                    for field in self._client.fields(ent):
                        selects.append(field)
                except influxdb.exceptions.InfluxDBClientError:
                    selects = ["*"]
        return selects

    @property
    def _from(self):
        return str(self.measurement)

    @property
    def _where(self):
        for exp in self._expressions:
            yield "(%s)" % exp
