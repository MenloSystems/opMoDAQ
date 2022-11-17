"""
Monitoring, control and operation mode configuration of
Raspberry Pi DAQHATs.
"""

import atexit
import functools
import importlib
import logging
import os
import pprint
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
from collections import namedtuple
from distutils.version import LooseVersion
from pathlib import Path

# Get the version from the _version.py versioneer file. For a git checkout,
# this is computed based on the number of commits since the last tag.
from opmodaq._version import get_versions

__version__ = str(get_versions()['version'])
del get_versions

_log = logging.getLogger(__name__)

_ExecInfo = namedtuple("_ExecInfo", "executable version")

def opmodaq_fname():
    """
    Get the location of the config file.

    The file location is determined in the following order

    - ``$PWD/opmodaqrc``
    - ``$OPMODAQRC`` if it is not a directory
    - ``$OPMODAQRC/opmodaqrc``
    - ``$MPLCONFIGDIR/opmodaqrc``
    - On Linux,
        - ``$XDG_CONFIG_HOME/opmodaq/opmodaqrc`` (if ``$XDG_CONFIG_HOME``
          is defined)
        - or ``$HOME/.config/opmodaq/opmodaqrc`` (if ``$XDG_CONFIG_HOME``
          is not defined)
    - On other platforms,
      - ``$HOME/.opmodaq/opmodaqrc`` if ``$HOME`` is defined
    - Lastly, it looks in ``$OPMODAQDATA/opmodaqrc``, which should always
      exist.
    """

    def gen_candidates():
        yield os.path.join(os.getcwd(), 'opmodaqrc')
        try:
            opmodaqrc = os.environ['OPMODAQRC']
        except KeyError:
            pass
        else:
            yield opmodaqrc
            yield os.path.join(opmodaqrc, 'opmodaqrc')
        # yield os.path.join(get_configdir(), 'opmodaqrc')
        # yield os.path.join(_get_data_path(), 'opmodaqrc')

    for fname in gen_candidates():
        if os.path.exists(fname) and not os.path.isdir(fname):
            return fname

    raise RuntimeError("Could not find opmodaqrc file")

# def rc_params(fail_on_error = False):
#     """Construct a `RcParams` instance from the default rc file."""
#     return rc_params_from_file(opmodaq_config_path(), fail_on_error)
