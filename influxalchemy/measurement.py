""" InfluxDB Measurement. """

import sys

if sys.version_info.major >= 3:
    # pylint: disable=import-error,unused-import
    from .measurement3 import Measurement
else:
    # pylint: disable=unused-import
    from .measurement2 import Measurement
