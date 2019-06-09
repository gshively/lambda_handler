import pkgutil
import importlib
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

for ( module_loader, name, ispkg) in pkgutil.iter_modules([Path(__file__).parent]):
    """ Import all modules under the resources """
    logger.info(f'Importing resource "{name}" from "{module_loader.path}"')
    importlib.import_module('.' + name, __package__)

