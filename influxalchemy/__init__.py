""" InfluxDB Alchemy. """
import pkg_resources

from .client import InfluxAlchemy
from .measurement import Measurement


try:
    __version__ = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    __version__ = None                      # pragma: no cover
