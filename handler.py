#!/usr/bin/env python3

from resources import Resource

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
    request_type  = event['RequestType']
    resource_type = event['ResourceType'].split('::')[-1]

    for subclass in Resource.__subclasses__():
        if subclass.resource_type() == resource_type:

            resource = subclass.init_from_event(event, context)
            print(resource)

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

class L:
    @classmethod
    def handler(cls, e, c):
        print('Here')

if __name__ == '__main__':

    h = L.handler
    h({'e':1}, {})
    cfn_handler({
        'RequestType': 'Update',
        'ResourceType': 'Custom::HostedZone',
    }, {})
    cfn_handler({
        'RequestType': 'Update',
        'ResourceType': 'Custom::HealthCheck',
    }, {})
