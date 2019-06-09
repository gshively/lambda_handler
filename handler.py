#!/usr/bin/env python3

from lambdahandler import LambdaHandler


def handler(event, context):
    lambda_handler = LambdaHandler(event, context)
    lambda_handler.process_event()


if __name__ == '__main__':
    handler({
        'StackId': 'arn:asdasdsadasd',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HostedZone',
    }, {})

    """
    cfn_handler({
        'RequestType': 'Create',
        'ResourceType': 'Custom::HostedZone',
    }, {})
    cfn_handler({
        'RequestType': 'Create',
        'ResourceType': 'Custom::HealthCheck',
    }, {})
    """
