""" Test Operations. """

from nose import tools
from influxalchemy.operations import Operation


def test_op_init():
    op = Operation(" fizz ", " buzz ")
    yield tools.assert_equal, op._op, " fizz "
    yield tools.assert_equal, op._nop, " buzz "


def test_op_str():
    op = Operation(" fizz ", " buzz ")
    yield tools.assert_equal, str(op), " fizz "


def test_op_repr():
    op = Operation(" fizz ", " buzz ")
    yield tools.assert_equal, repr(op), " fizz "


def test_op_inv():
    op = ~Operation(" fizz ", " buzz ")
    yield tools.assert_equal, op._nop, " fizz "
    yield tools.assert_equal, op._op, " buzz "


def test_op_eq():
    op0 = Operation(" fizz ", " buzz ")
    op1 = Operation(" fizz ", " buzz ")
    yield tools.assert_equal, op0, op1


def test_op_ne():
    op0 = Operation(" fizz ", " buzz ")
    op1 = ~op0
    yield tools.assert_not_equal, op0, op1
