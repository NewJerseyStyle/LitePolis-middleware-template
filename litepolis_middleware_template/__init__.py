from .core import add_middleware
# Import configuration
from .utils import DEFAULT_CONFIG

# Define what gets imported when using 'from package import *'
__all__ = [
    "DEFAULT_CONFIG",
    "add_middleware"
]