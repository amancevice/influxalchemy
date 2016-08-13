""" Python2 Measurement. """

from . import meta


# pylint: disable=too-few-public-methods
class Measurement(object):
    """ InfluxDB Measurement. """
    __metaclass__ = meta.MetaMeasurement

    @classmethod
    def new(cls, name):
        """ Generate new Measurement class. """
        return type(name, (cls,), {"__measurement__": name})
