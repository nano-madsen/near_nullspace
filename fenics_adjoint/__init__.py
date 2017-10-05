__version__ = '0.0.1'
__author__  = 'Sebastian Kenji Mitusch'
__credits__ = []
__license__ = 'LGPL-3'
__maintainer__ = 'Sebastian Kenji Mitusch'
__email__ = 'sebastkm@math.uio.no'

import sys
if not 'backend' in sys.modules:
    import fenics
    sys.modules['backend'] = fenics
backend = sys.modules['backend']

if backend.__name__ != "firedrake":
    from .types import genericmatrix

from .ui import *
