#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)
from enum import Enum

import cfnresponse

from customresource import CustomResource
import resources

class InvalidRequestType(Exception): pass
class InvalidResourceType(Exception): pass

class LambdaHandler:

    def __init__(self, event, context):
        self.event = event
        self.context = context

        self.logger = logging.getLogger(self.__class__.__name__)

    def send_response(self, status, reason=None, resource=None):
        """Send response back to CFN Url"""

        self.logger.debug( 'cfnresponse.send("%s", %s, "%s", "%s")',
            status,
            f'"{reason}"' if reason else 'None',
            f'"{resource.data}"' if resource and resource.data else 'None',
            f'"{resource.physical_id}"' if resource and resource.physical_id else 'None'
        )
        """
        cfnresponse.send(
            self.event,
            self.context,
            status,
            reason,
            resource or resource.data,
            resource or resource.resource_id
        )
        """

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
                self.logger.debug(f'Initializing resource {resource}')

                if request_type == 'Create':
                    resource.create()
                elif request_type == 'Update':
                    resource.update()
                elif request_type == 'Delete':
                    resource.delete()
                else:
                    raise InvalidRequestType(request_type)

                self.send_response('SUCCESS', resource=resource)
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
                self.send('FAILURE', reason=str(e))
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
