""" InfluxAlchemy Measurements. """

from influxalchemy.measurement import Measurement
from influxalchemy.meta import Tag
from influxalchemy.meta import TagExp
from influxalchemy.operations import *
from nose import tools


def test_meta_getattr():
    meas = Measurement.new("fizz")
    yield tools.assert_equal, meas.buzz, Tag("buzz", meas)


def test_meta_str():
    meas = Measurement.new("fizz")
    yield tools.assert_equal, str(meas), "fizz"


def test_meta_ne():
    meas0 = Measurement.new("fizz")
    meas1 = Measurement.new("buzz")
    yield tools.assert_true, meas0 != meas1


def test_meta_or():
    meas0 = Measurement.new("fizz")
    meas1 = Measurement.new("buzz")
    yield tools.assert_equal, (meas0 | meas1), Measurement.new("/fizz|buzz/")


def test_meta_measurement():
    meas = Measurement.new("fizz")
    yield tools.assert_equal, meas, meas.measurement


class Fizz(Measurement):
    __measurement__ = "fizz"


def test_new():
    yield tools.assert_equal, Measurement.new("fizz"), Fizz


def test_tag_init():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    yield tools.assert_equal, tag, meas.buzz


def test_tag_str():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    yield tools.assert_equal, str(tag), "buzz"


def test_tag_repr():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    yield tools.assert_equal, repr(tag), "<fizz.buzz>"


def test_tag_eq():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag == "foo"
    yield tools.assert_equal, exp, TagExp("buzz", EQ, "foo")


def test_tag_ne():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag != "foo"
    yield tools.assert_equal, exp, TagExp("buzz", NE, "foo")


def test_tag_gt():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag > "foo"
    yield tools.assert_equal, exp, TagExp("buzz", GT, "foo")


def test_tag_lt():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag < "foo"
    yield tools.assert_equal, exp, TagExp("buzz", LT, "foo")


def test_tag_ge():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag >= "foo"
    yield tools.assert_equal, exp, TagExp("buzz", GE, "foo")


def test_tag_le():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag <= "foo"
    yield tools.assert_equal, exp, TagExp("buzz", LE, "foo")


def test_tag_like():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag.like("foo")
    yield tools.assert_equal, exp, TagExp("buzz", LK, "foo")


def test_tag_notlike():
    meas = Measurement.new("fizz")
    tag = Tag("buzz", meas)
    exp = tag.notlike("foo")
    yield tools.assert_equal, exp, TagExp("buzz", NK, "foo")


def test_time_between():
    meas = Measurement.new("fizz")
    exp = meas.time.between("'2016-01-01'", "now() - 7d")
    yield tools.assert_equal, exp, \
        TagExp(meas.time, " >= ", "'2016-01-01'") & \
        TagExp(meas.time, " <= ", "now() - 7d")


def test_time_between_excl():
    meas = Measurement.new("fizz")
    exp = meas.time.between("'2016-01-01'", "now() - 7d", False, False)
    yield tools.assert_equal, exp, \
        TagExp(meas.time, " > ", "'2016-01-01'") & \
        TagExp(meas.time, " < ", "now() - 7d")


def test_exp_init():
    meas = Measurement.new("fizz")
    exp = TagExp(meas.buzz, " = ", "goo")
    yield tools.assert_equal, exp._left, meas.buzz
    yield tools.assert_equal, exp._op, " = "
    yield tools.assert_equal, exp._right, "'goo'"


def test_exp_str():
    meas = Measurement.new("fizz")
    exp = TagExp(meas.buzz, " = ", "goo")
    yield tools.assert_equal, str(exp), "buzz = 'goo'"


def test_exp_repr():
    meas = Measurement.new("fizz")
    exp = TagExp(meas.buzz, " = ", "goo")
    yield tools.assert_equal, repr(exp), "[ buzz = 'goo' ]"


def test_exp_ne():
    meas = Measurement.new("fizz")
    exp0 = TagExp(meas.buzz, " = ", "goo")
    exp1 = TagExp(meas.guzz, " = ", "zoo")
    yield tools.assert_true, exp0 != exp1


def test_exp_and():
    meas = Measurement.new("fizz")
    exp0 = TagExp(meas.buzz, " = ", "goo")
    exp1 = TagExp(meas.guzz, " = ", "zoo")
    yield tools.assert_equal, (exp0 & exp1), \
        TagExp("buzz = 'goo'", " AND ", "guzz = 'zoo'")


def test_exp_or():
    meas = Measurement.new("fizz")
    exp0 = TagExp(meas.buzz, " = ", "goo")
    exp1 = TagExp(meas.guzz, " = ", "zoo")
    yield tools.assert_equal, (exp0 | exp1), \
        TagExp("buzz = 'goo'", " OR ", "guzz = 'zoo'")


def test_exp_inv():
    meas = Measurement.new("fizz")
    exp = TagExp(meas.buzz, EQ, "goo")
    yield tools.assert_equal, ~exp, TagExp(meas.buzz, NE, "'goo'")


def test_equals():
    meas = Measurement.new("fizz")
    exp = TagExp.equals(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, EQ, "goo")


def test_notequals():
    meas = Measurement.new("fizz")
    exp = TagExp.notequals(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, NE, "goo")


def test_greater_than():
    meas = Measurement.new("fizz")
    exp = TagExp.greater_than(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, GT, "goo")


def test_less_than():
    meas = Measurement.new("fizz")
    exp = TagExp.less_than(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, LT, "goo")


def test_greater_equal():
    meas = Measurement.new("fizz")
    exp = TagExp.greater_equal(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, GE, "goo")


def test_less_equal():
    meas = Measurement.new("fizz")
    exp = TagExp.less_equal(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, LE, "goo")


def test_like():
    meas = Measurement.new("fizz")
    exp = TagExp.like(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, LK, "goo")


def test_notlike():
    meas = Measurement.new("fizz")
    exp = TagExp.notlike(meas.buzz, "goo")
    yield tools.assert_equal, exp, TagExp(meas.buzz, NK, "goo")
