from .resource import Resource
import pkgutil
import importlib
from pathlib import Path

__all__ = []

for ( module_loader, name, ispkg) in pkgutil.iter_modules([Path(__file__).parent]):
    importlib.import_module('.' + name, __package__)

for subclass in Resource.__subclasses__():
    globals()[subclass.__name__] = subclass
    __all__.append(name)

