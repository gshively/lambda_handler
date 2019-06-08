import pkgutil
import importlib
from pathlib import Path

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Resource:

    @classmethod
    def init_from_event(cls, event, context):
        obj = cls()
        obj._event = event
        obj._context = context

        return obj

    @classmethod
    def resource_type(cls):
        return cls.__name__

    def create(self):
        logger.debug(f'{self.__class__.__name__} create')

    def update(self):
        logger.debug(f'{self.__class__.__name__} update')

    def delete(self):
        logger.debug(f'{self.__class__.__name__} delete')

    @property
    def physical_id(self):
        return self._event.get('PhysicalResourceId')

    @property
    def response_data(self):
        return {}
        

for ( module_loader, name, ispkg) in pkgutil.iter_modules([Path(__file__).parent]):
    """ Import all modules under the resources """
    logger.debug(f'Importing resource {name}')
    importlib.import_module('.' + name, __package__)


def all_resources():
    for resource in Resource.__subclasses__():
        yield resource


