""" InfluxDB Measurement. """

from . import operations


class MetaMeasurement(type):
    def __getattr__(self, name):
        if name == "time":
            return Time(name, self)
        else:
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

    @property
    def measurement(self):
        return self


class Measurement(object):
    __metaclass__ = MetaMeasurement

    @classmethod
    def new(cls, name):
        return type(name, (cls,), {"__measurement__": name})


class Tag(object):
    def __init__(self, name, measurement):
        self._name = name
        self.measurement = measurement

    def __repr__(self):
        return "<%s.%s>" % (self.measurement.__measurement__, self._name)

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


class Time(Tag):
    def between(self, start, end, startinc=True, endinc=True):
        if startinc is True:
            startexp = TagExp.ge(self, start)
        else:
            startexp = TagExp.gt(self, start)
        if endinc is True:
            endexp = TagExp.le(self, end)
        else:
            endexp = TagExp.lt(self, end)
        return startexp & endexp


class TagExp(object):
    def __init__(self, left, op, right):
        self._left = left
        self._op = op
        lits = [operations.LK, operations.NK, operations.AND, operations.OR]
        if self._op in lits or isinstance(left, Time):
            self._right = right
        else:
            self._right = repr(right)

    def __repr__(self):
        return "[ %s ]" % self

    def __str__(self):
        return "%s%s%s" % (self._left, self._op, self._right)

    def __and__(self, other):
        return TagExp(str(self), " AND ", str(other))

    def __or__(self, other):
        return TagExp(str(self), " OR ", str(other))

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
        return TagExp(self, operations.LK, other)

    @classmethod
    def nk(cls, self, other):
        return TagExp(self, operations.NK, other)
