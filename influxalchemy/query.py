""" InfluxDB Query Object. """
import functools

from . import meta


class InfluxDBQuery(object):
    """ InfluxDB Query object.

        entities    (tuple):          Query entities
        client      (InfluxAlchemy):  InfluxAlchemy instance
        expressions (tuple):          Query filters
        groupby     (str):            GROUP BY string
        limit       (int):            LIMIT int
        orderby_asc (str):            ORDER BY string ASC (ascending order)
        orderby_desc(str):            ORDER BY string DESC (descending order)
    """
    def __init__(self, entities, client, expressions=None, groupby=None,
                 limit=None, orderby_asc=None, orderby_desc=None):
        # pylint: disable=too-many-arguments
        self._entities = entities
        self._client = client
        self._expressions = expressions or ()
        self._groupby = groupby
        self._limit = limit
        self._orderby_asc = orderby_asc
        self._orderby_desc = orderby_desc

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
        if self._limit is not None:
            iql += " LIMIT {0}".format(self._limit)
        if self._orderby_asc is not None:
            iql += " ORDER BY %s ASC" % self._orderby_asc
        elif self._orderby_desc is not None:
            iql += " ORDER BY %s DESC" % self._orderby_desc
        return "%s;" % iql

    def __repr__(self):
        return str(self)

    def execute(self):
        """ Execute query. """
        return self._client.bind.query(str(self))

    def filter(self, *expressions):
        """ Filter query. """
        expressions = self._expressions + expressions
        return InfluxDBQuery(self._entities, self._client,
                             expressions=expressions)

    def filter_by(self, **kwargs):
        """ Filter query by tag value. """
        expressions = self._expressions
        for key, val in sorted(kwargs.items()):
            expressions += (meta.TagExp.equals(key, val),)
        return InfluxDBQuery(self._entities, self._client,
                             expressions=expressions)

    def group_by(self, groupby):
        """ Group query. """
        return InfluxDBQuery(
            self._entities, self._client, self._expressions, groupby)

    def limit(self, limit):
        """ Limit query """
        assert isinstance(limit, int)
        return InfluxDBQuery(
            self._entities, self._client, self._expressions, self._groupby,
            limit)

    def order_by_asc(self, orderby_asc):
        """ Ascending order query. """
        return InfluxDBQuery(
            self._entities, self._client, self._expressions, self._groupby,
            self._limit, orderby_asc=orderby_asc)

    def order_by_desc(self, orderby_desc):
        """ Descending order query. """
        return InfluxDBQuery(
            self._entities, self._client, self._expressions, self._groupby,
            self._limit, orderby_desc=orderby_desc)

    @property
    def measurement(self):
        """ Query measurement. """
        measurements = set(x.measurement for x in self._entities)
        return functools.reduce(lambda x, y: x | y, measurements)

    @property
    def _select(self):
        """ SELECT statement. """
        selects = []
        for ent in self._entities:
            # Entity is a Tag
            if isinstance(ent, meta.Tag):
                selects.append(str(ent))
            # Entity is a Measurement
            else:
                try:
                    for tag in self._client.tags(ent):
                        selects.append(tag)
                    for field in self._client.fields(ent):
                        selects.append(field)
                # pylint: disable=broad-except
                except Exception:
                    pass
        return selects or ["*"]

    @property
    def _from(self):
        """ FROM statement. """
        return str(self.measurement)

    @property
    def _where(self):
        """ WHERE statement. """
        for exp in self._expressions:
            yield "(%s)" % exp
