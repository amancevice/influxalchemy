""" InfluxDB Measurement. """

from . import operations


class MetaMeasurement(type):
    def __getattr__(self, name):
        return Tag(name, self)

    def __str__(self):
        try:
            return self.__measurement__
        except AttributeError:
            return self.__name__

    def __or__(self, other):
        left = str(self).strip("/")
        name = "_".join(left.split("|") + [str(other)])
        bases = Measurement,
        measurement = "/%s|%s/" % (str(self).strip("/"), other)
        return type(name, bases, {"__measurement__": measurement})

    def tags(self, client):
        tags = client.query("SHOW tag keys FROM %s" % self)
        for tag in tags.get_points():
            for val in tag.values():
                yield val

    def fields(self, client):
        fields = client.query("SHOW field keys FROM %s" % self)
        for field in fields.get_points():
            for val in field.values():
                yield val

    @property
    def measurement(self):
        return self


class Measurement(object):
    __metaclass__ = MetaMeasurement

    @classmethod
    def generate(cls, name):
        return type(name, (cls,), {"__measurement__": name})


class Tag(object):
    def __init__(self, name, measurement):
        self._name = name
        self.measurement = measurement

    def __repr__(self):
        return "<%s.%s>" % (self._measurement.__measurement__, self._name)

    def __str__(self):
        return self._name

    def __eq__(self, other):
        return TagExp.eq(self, other)

    def __ne__(self, other):
        return TagExp.ne(self, other)

    def __gt__(self, other):
        return TagExp.gt(self, other)

    def __lt__(self, other):
        return TagExp.lt(self, other)

    def __ge__(self, other):
        return TagExp.ge(self, other)

    def __le__(self, other):
        return TagExp.le(self, other)

    def like(self, other):
        return TagExp.lk(self, other)

    def notlike(self, other):
        return TagExp.nk(self, other)


class TagExp(object):
    def __init__(self, left, op, right, exp="%s%s%r"):
        self._left = left
        self._op = op
        self._right = right
        self._exp = exp

    def __repr__(self):
        return "[ %s ]" % self

    def __str__(self):
        return self._exp % (self._left, self._op, self._right)

    def __and__(self, other):
        return TagExp(str(self), " AND ", str(other), "%s%s%s")

    def __or__(self, other):
        return TagExp(str(self), " OR ", str(other), "%s%s%s")

    def __invert__(self):
        return TagExp(self._left, ~self._op, self._right)

    @classmethod
    def eq(cls, self, other):
        return TagExp(self, operations.EQ, other)

    @classmethod
    def ne(cls, self, other):
        return TagExp(self, operations.NE, other)

    @classmethod
    def gt(cls, self, other):
        return TagExp(self, operations.GT, other)

    @classmethod
    def lt(cls, self, other):
        return TagExp(self, operations.LT, other)

    @classmethod
    def ge(cls, self, other):
        return TagExp(self, operations.GE, other)

    @classmethod
    def le(cls, self, other):
        return TagExp(self, operations.LE, other)

    @classmethod
    def lk(cls, self, other):
        return TagExp(self, operations.LK, other, "%s%s%s")

    @classmethod
    def nk(cls, self, other):
        return TagExp(self, operations.NK, other, "%s%s%s")
