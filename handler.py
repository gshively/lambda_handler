#!/usr/bin/env python3

import logging
import resources


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class InvalidRequestType: pass

def cfn_send(event, context, status, physical_id, resource_data):
    pass

def send_fail(event, context, resource):
    cfn_send(event, context, 'fail', None, None)

def send_success(event, context, resource):
    resource_id = resource.physical_id
    response_data = resource.response_data

    cfn_send(event, context, 'success', resource_id, response_data)

def invoke_handler(event, context):
    raise NotImplementedError

def cfn_handler(event, context):
    logging.debug(f'CFN Handler: {event}')
    request_type  = event['RequestType']
    resource_type = event['ResourceType'].split('::')[-1]

    for subclass in resources.all_resources():
        logger.debug(f'Checking if {resource_type} matches {subclass}\'s resource type')
        if subclass.resource_type() == resource_type:

            resource = subclass.init_from_event(event, context)
            logger.debug(f'init resource {resource}')

            if request_type == 'Create':
                resource.create()
            elif request_type == 'Update':
                resource.update()
            elif request_type == 'Delete':
                resource.delete()
            else:
                raise InvalidRequestType

            send_success(event, context, resource)


def handler(event, context):
    try:
        if 'StackId' in event:
            cfn_handler(event, context)
        else:
            invoke_handler(event, context)
    except Exception as e:
        if 'ResponseURL' in event:
            send(event, context)
        raise

if __name__ == '__main__':

    cfn_handler({
        'RequestType': 'Create',
        'ResourceType': 'Custom::HostedZone',
    }, {})
    cfn_handler({
        'RequestType': 'Create',
        'ResourceType': 'Custom::HealthCheck',
    }, {})
