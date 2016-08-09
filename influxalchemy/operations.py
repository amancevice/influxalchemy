""" InfluxDB Operations. """


class Operation(object):
    def __init__(self, op, nop):
        self._op = op
        self._nop = nop

    def __str__(self):
        return self._op

    def __repr__(self):
        return str(self)

    def __invert__(self):
        return Operation(self._nop, self._op)


EQ = Operation(" = ", " != ")
NE = Operation(" != ", " = ")
GT = Operation(" > ", " <= ")
LT = Operation(" < ", " >= ")
GE = Operation(" >= ", " < ")
LE = Operation(" <= ", " > ")
LK = Operation(" =~ ", " !~ ")
NK = Operation(" !~ ", " =~ ")
