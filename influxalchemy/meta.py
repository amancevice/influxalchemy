""" InfluxDB Meta Measurement. """
from datetime import date

from . import operations

try:
    from datetime import timezone
    UTC = timezone.utc  # pragma: no cover
except ImportError:     # pragma: no cover
    import pytz         # pragma: no cover
    UTC = pytz.utc      # pragma: no cover


def make_tz_aware(datetime_obj):
    """ Make a date/datetime object to be timezone-aware """
    # 'date' object doesn't need to be timezone aware
    # pylint: disable=unidiomatic-typecheck
    if type(datetime_obj) is date:
        return datetime_obj
    # Already aware
    if datetime_obj.tzinfo:
        return datetime_obj
    # With naive datetime object, assume it is UTC
    return datetime_obj.replace(tzinfo=UTC)


class MetaMeasurement(type):
    """ Meta class of Measurement. """
    def __new__(cls, name, bases, dict_):
        dict_.setdefault("__measurement__", name)
        return super(MetaMeasurement, cls).__new__(cls, name, bases, dict_)

    def __getattribute__(cls, name):
        try:
            return super(MetaMeasurement, cls).__getattribute__(name)
        except AttributeError:
            if name == "time":
                return Time(name, cls)
            return Tag(name, cls)

    def __str__(cls):
        return cls.__measurement__

    def __eq__(cls, other):
        return str(cls) == str(other)

    def __ne__(cls, other):
        return str(cls) != str(other)

    def __or__(cls, other):
        left = str(cls).strip("/")
        name = "_".join(left.split("|") + [str(other)])
        bases = (cls,)
        measurement = "/%s|%s/" % (str(cls).strip("/"), other)
        return type(name, bases, {"__measurement__": measurement})

    def __hash__(cls):
        return id(cls)

    @property
    def measurement(cls):
        """ Reflexive reference to measurement. """
        return cls


class Tag(object):
    """ InfluxDB Tag instance.

        name        (str):          Name of Tag
        measurement (Measurement):  Measurement of tag
    """
    def __init__(self, name, measurement):
        self._name = name
        self.measurement = measurement

    def __str__(self):
        return self._name

    def __repr__(self):
        return "<%s.%s>" % (self.measurement.__measurement__, self._name)

    def __eq__(self, other):
        return TagExp.equals(self, other)

    def __ne__(self, other):
        return TagExp.notequals(self, other)

    def __gt__(self, other):
        return TagExp.greater_than(self, other)

    def __lt__(self, other):
        return TagExp.less_than(self, other)

    def __ge__(self, other):
        return TagExp.greater_equal(self, other)

    def __le__(self, other):
        return TagExp.less_equal(self, other)

    def like(self, other):
        """ self =~ other """
        return TagExp.like(self, other)

    def notlike(self, other):
        """ self !~ other """
        return TagExp.notlike(self, other)


class Time(Tag):
    """ Time of InfluxDB Measurement. """
    def between(self, start, end, startinc=True, endinc=True):
        """ Query times between extremes.

            Arguments:
                start    (str):      Start of time
                end      (str):      End of time
                startinc (boolean):  Start-inclusive flag
                endinc   (boolean):  End-inclusive flag

            Returns:
                Time expression.
        """
        if startinc is True:
            startexp = TagExp.greater_equal(self, start)
        else:
            startexp = TagExp.greater_than(self, start)
        if endinc is True:
            endexp = TagExp.less_equal(self, end)
        else:
            endexp = TagExp.less_than(self, end)
        return startexp & endexp


class TagExp(object):
    """ A tag query expression. """
    def __init__(self, left, op, right):
        self._left = left
        self._op = op
        lits = [operations.LK, operations.NK, operations.AND, operations.OR]
        if self._op in lits or isinstance(left, Time):
            # If the right-hand-side value is a date/datetime object,
            # we convert it to RFC3339 representation
            # and wrap inside single quote
            if isinstance(right, date):
                right = repr(make_tz_aware(right).isoformat())
            self._right = right
        else:
            self._right = repr(right)

    def __str__(self):
        return "%s%s%s" % (self._left, self._op, self._right)

    def __repr__(self):
        return "[ %s ]" % self

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)

    def __and__(self, other):
        return TagExp(str(self), " AND ", str(other))

    def __or__(self, other):
        return TagExp(str(self), " OR ", str(other))

    def __invert__(self):
        return TagExp(self._left, ~self._op, self._right)

    @classmethod
    def equals(cls, self, other):
        """ left = right """
        return cls(self, operations.EQ, other)

    @classmethod
    def notequals(cls, self, other):
        """ left != right """
        return cls(self, operations.NE, other)

    @classmethod
    def greater_than(cls, self, other):
        """ left > right """
        return cls(self, operations.GT, other)

    @classmethod
    def less_than(cls, self, other):
        """ left < right """
        return cls(self, operations.LT, other)

    @classmethod
    def greater_equal(cls, self, other):
        """ left >= right """
        return cls(self, operations.GE, other)

    @classmethod
    def less_equal(cls, self, other):
        """ left <= right """
        return cls(self, operations.LE, other)

    @classmethod
    def like(cls, self, other):
        """ left =~ right """
        return cls(self, operations.LK, other)

    @classmethod
    def notlike(cls, self, other):
        """ left !~ right """
        return cls(self, operations.NK, other)
