""" Python3 Measurement. """

# pylint: disable=unused-import
from . import meta


# pylint: disable=too-few-public-methods
class Measurement(metaclass=meta.MetaMeasurement):
    """ InfluxDB Measurement. """
    @classmethod
    def new(cls, name):
        """ Generate new Measurement class. """
        return type(name, (cls,), {"__measurement__": name})
