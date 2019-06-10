#!/usr/bin/env python3

import logging
import logging_config
logger = logging.getLogger()

from lambdahandler import LambdaHandler

class DnsHandler(LambdaHandler):
    pass

def handler(event, context):
    DnsHandler(event, context).process_event()


if __name__ == '__main__':
    logger.warn('Processing __main__')
    handler({
        'StackId': 'arn',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HostedZone',
    }, {})
    handler({
        'StackId': 'arn',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HealthCheck',
    }, {})
