from .base import *

# Load environment-specific settings
try:
    from .local import *
except ImportError:
    pass
