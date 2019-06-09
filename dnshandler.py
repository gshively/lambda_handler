#!/usr/bin/env python3

import logging_config

from lambdahandler import LambdaHandler

class DnsHandler(LambdaHandler):
    pass

def handler(event, context):
    DnsHandler(event, context).processevent()


if __name__ == '__main__':

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
