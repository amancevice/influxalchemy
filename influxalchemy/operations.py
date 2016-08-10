""" InfluxDB Operations. """


# pylint: disable=too-few-public-methods
class Operation(object):
    """ InfluxDB query operation. """
    def __init__(self, op, nop):
        self._op = op
        self._nop = nop

    def __str__(self):
        return self._op

    def __repr__(self):
        return str(self)

    def __invert__(self):
        return Operation(self._nop, self._op)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)


EQ = Operation(" = ", " != ")
NE = Operation(" != ", " = ")
GT = Operation(" > ", " <= ")
LT = Operation(" < ", " >= ")
GE = Operation(" >= ", " < ")
LE = Operation(" <= ", " > ")
LK = Operation(" =~ ", " !~ ")
NK = Operation(" !~ ", " =~ ")
AND = Operation(" AND ", " OR ")
OR = Operation(" OR ", " AND ")
