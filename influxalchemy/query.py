""" InfluxDB Query Object. """

import itertools

from . import measurement


class InfluxDBQuery(object):
    def __init__(self, entities, client, *expressions):
        self._entities = entities
        self._client = client
        self._expressions = expressions

    def __str__(self):
        select = ", ".join(self._select)
        from_ = self._from
        where = " AND ".join(self._where)
        if any(where):
            return "SELECT %s FROM %s WHERE %s;" % (select, from_, where)
        else:
            return "SELECT %s FROM %s;" % (select, from_)

    def __repr__(self):
        return str(self)

    def filter(self, *expressions):
        expressions = self._expressions + expressions
        return InfluxDBQuery(self._entities, self._client, *expressions)

    def filter_by(self, **kwargs):
        expressions = self._expressions
        for key, val in kwargs.items():
            expressions += measurement.TagExp.eq(key, val),
        return InfluxDBQuery(self._entities, self._client, *expressions)

    def execute(self):
        return self._client.bind.query(str(self))

    @property
    def measurement(self):
        measurements = set(x.measurement for x in self._entities)
        return reduce(lambda x, y: x | y, measurements)

    @property
    def _select(self):
        for ent in self._entities:
            # Entity is a Tag
            if isinstance(ent, measurement.Tag):
                yield str(ent)
            # Entity is a Measurement
            else:
                for tag in self._client.tags(ent):
                    yield tag
                for field in self._client.fields(ent):
                    yield field

    @property
    def _from(self):
        return str(self.measurement)

    @property
    def _where(self):
        for exp in self._expressions:
            yield "(%s)" % exp
