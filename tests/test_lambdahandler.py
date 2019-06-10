from hypothesis import given
from hypothesis.strategies import text
from unittest.mock import patch
from lambdahandler import LambdaHandler
from customresource import CustomResource

@given(text())
def test_stack_id_from_event(stack_id):
    handler = LambdaHandler({'StackId': stack_id}, {})
    assert handler.stack_id == stack_id

@given(text())
def test_stack_id_from_event(response_url):
    handler = LambdaHandler({'ResponseURL': response_url}, {})
    assert handler.response_url == response_url

@patch.object(LambdaHandler, 'invoke_handler')
def test_stack_id_not_set_calls_invoke_handler(invoke_handler):
    event = {}
    context = {} 
    handler = LambdaHandler(event, context)
    handler.process_event()

    assert invoke_handler.called

@patch.object(LambdaHandler, 'invoke_handler')
def test_stack_id_set_none_calls_invoke_handler(invoke_handler):
    event = {'StackId': None}
    context = {} 
    handler = LambdaHandler(event, context)
    handler.process_event()

    assert invoke_handler.called

@patch.object(LambdaHandler, 'cfn_handler')
def test_stack_id_set_calls_cfn_handler(cfn_handler):
    event = {'StackId': 'arn:aws:stack'}
    context = {} 
    handler = LambdaHandler(event, context)
    handler.process_event()

    assert cfn_handler.called


def test_resources():
    assert [t.resource_type() for t in CustomResource.all_resources()] is None


