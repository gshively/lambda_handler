#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)

from customresource import CustomResource
import resources

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
        self.event = event
        self.context = context

        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def stack_id(self):
        return self.event.get('StackId')

    @property
    def response_url(self):
        return self.event.get('ResponseURL')

    def invoke_handler(self):
        raise NotImplementedError

    def cfn_handler(self):
        self.logger.debug(f'CFN Handler: {self.event}')
        request_type  = self.event['RequestType']
        resource_type = self.event['ResourceType'].split('::')[-1]

        for subclass in CustomResource.all_resources():
            self.logger.debug(f'Checking if {resource_type} matches {subclass}\'s resource type')
            if subclass.resource_type() == resource_type:

                resource = subclass.init_from_event(self.event, self.context)
                self.logger.debug(f'init resource {resource}')

                if request_type == 'Create':
                    resource.create()
                elif request_type == 'Update':
                    resource.update()
                elif request_type == 'Delete':
                    resource.delete()
                else:
                    raise InvalidRequestType(request_type)

                send_success(self.event, self.context, resource)
                return

        raise InvalidResourceType(resource_type)

    @classmethod
    def handler(cls, event, context):
        cls(event, context).processevent()

    def processevent(self):

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
