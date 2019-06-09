import pkgutil
import importlib
from pathlib import Path

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


for ( module_loader, name, ispkg) in pkgutil.iter_modules([Path(__file__).parent]):
    """ Import all modules under the resources """
    logger.debug(f'Importing resource {name}')
    importlib.import_module('.' + name, __package__)

