#!/usr/bin/env python3

import logging
from customresource import CustomResource
import resources


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class InvalidRequestType(Exception): pass
class InvalidResourceType(Exception): pass

def cfn_send(event, context, status, physical_id, resource_data):
    pass

def send_fail(event, context, resource):
    cfn_send(event, context, 'fail', None, None)

def send_success(event, context, resource):
    resource_id = resource.physical_id
    response_data = resource.response_data

    cfn_send(event, context, 'success', resource_id, response_data)

class LambdaHandler:

    def __init__(self, event, context):
        self._event = event
        self._context = context

    @property
    def stack_id(self):
        return self._event.get('StackId')

    @property
    def response_url(self):
        return self._event.get('ResponseURL')

    def invoke_handler(self):
        raise NotImplementedError

    def cfn_handler(self):
        logging.debug(f'CFN Handler: {self._event}')
        request_type  = self._event['RequestType']
        resource_type = self._event['ResourceType'].split('::')[-1]

        for subclass in CustomResource.all_resources():
            logger.debug(f'Checking if {resource_type} matches {subclass}\'s resource type')
            if subclass.resource_type() == resource_type:

                resource = subclass.init_from_event(self._event, self._context)
                logger.debug(f'init resource {resource}')

                if request_type == 'Create':
                    resource.create()
                elif request_type == 'Update':
                    resource.update()
                elif request_type == 'Delete':
                    resource.delete()
                else:
                    raise InvalidRequestType(request_type)

                send_success(self._event, self._context, resource)
                return

        raise InvalidResourceType(resource_type)

    @classmethod
    def handler(cls, event, context):
        cls(event, context).process_event()

    def process_event(self):

        try:
            if self.stack_id:
                self.cfn_handler()
            else:
                self.invoke_handler()

        except Exception as e:
            if self.response_url:
                self.send(event, context)
            raise

if __name__ == '__main__':

    LambdaHandler.handler({
        'StackId': 'arn',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HostedZone',
    }, {})
    LambdaHandler.handler({
        'StackId': 'arn',
        'RequestType': 'Create',
        'ResourceType': 'Custom::HealthCheck',
    }, {})
