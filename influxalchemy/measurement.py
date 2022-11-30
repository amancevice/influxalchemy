"""
InfluxDB Measurement.
"""
import six

from influxalchemy import meta


# pylint: disable=too-few-public-methods
class Measurement(six.with_metaclass(meta.MetaMeasurement)):
    """
    InfluxDB Measurement.
    """

    # pylint: disable=no-init
    @classmethod
    def new(cls, name):
        """
        Generate new Measurement class.
        """
        return type(name, (cls,), {"__measurement__": name})
