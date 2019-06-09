import os
import logging
from logging.config import dictConfig

DEFAULT_LOGLEVEL='DEBUG'

logging_config = dict(
    version=1,
    formatters={
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
	'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': getattr(
                logging, 
                (os.getenv('LOGLEVEL') or DEFAULT_LOGLEVEL).upper()
            ),
        }
    },
    loggers={
        'logging_config': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'resources': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'boto3': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'botocore': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'requests': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'urllib3': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },

    },
    root={
        'level': 'DEBUG',
        'handlers': ['console'],
    }
)

try:
    import colorlog
    logging_config['formatters']['color'] = {
        'class': 'colorlog.ColoredFormatter',
        'format': '%(green)s%(asctime)-20s%(reset)s%(log_color)s%(levelname)-8s%(reset)s %(blue)s[%(name)s]%(reset)s %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    logging_config['handlers']['console']['formatter'] = 'color'
except:
    pass

dictConfig(logging_config)
logger = logging.getLogger(__name__)
logger.debug('Logging Configured from dictConfig located "%s"', __file__)

