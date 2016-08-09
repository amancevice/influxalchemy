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

    def execute(self):
        return self._client.query(str(self))

    @property
    def _select(self):
        if len(self._entities) == 1 \
                and isinstance(self._entities[0], measurement.MetaMeasurement):
            yield "*"
        else:
            for ent in self._entities:
                try:
                    if issubclass(ent, measurement.Measurement):
                        for tag in ent.tags(self._client):
                            yield tag
                        for field in ent.fields(self._client):
                            yield field
                except TypeError:
                    yield str(ent)

    @property
    def _from(self):
        measurements = set(x.measurement for x in self._entities)
        measurement = reduce(lambda x, y: x | y, measurements)
        return str(measurement)

    @property
    def _where(self):
        for exp in self._expressions:
            yield str(exp)
