#!/usr/bin/env python3

import logging_config

from lambdahandler import LambdaHandler

class DnsHandler(LambdaHandler):
    pass

if __name__ == '__main__':

    DnsHandler.handler({
        'StackId': 'arn',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HostedZone',
    }, {})
    DnsHandler.handler({
        'StackId': 'arn',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HealthCheck',
    }, {})
