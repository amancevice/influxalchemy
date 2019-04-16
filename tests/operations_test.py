""" InfluxAlchemy Operations. """
from influxalchemy.operations import Operation


def test_op_init():
    op = Operation(" fizz ", " buzz ")
    assert op._op == " fizz "
    assert op._nop == " buzz "


def test_op_str():
    op = Operation(" fizz ", " buzz ")
    assert str(op) == " fizz "


def test_op_repr():
    op = Operation(" fizz ", " buzz ")
    assert repr(op) == " fizz "


def test_op_inv():
    op = ~Operation(" fizz ", " buzz ")
    assert op._nop == " fizz "
    assert op._op == " buzz "


def test_op_eq():
    op0 = Operation(" fizz ", " buzz ")
    op1 = Operation(" fizz ", " buzz ")
    assert op0 == op1


def test_op_ne():
    op0 = Operation(" fizz ", " buzz ")
    op1 = ~op0
    assert op0 != op1
