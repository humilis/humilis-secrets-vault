# -*- coding: utf-8 -*-
"""
Tests the logic of the Lambda function
"""

import inspect
import os
import sys
# Add the lambda directory to the python library search path
lambda_dir = os.path.join(
    os.path.dirname(inspect.getfile(inspect.currentframe())),
    '..', '..', 'lambda_function')
sys.path.append(lambda_dir)

import uuid
from mock import Mock

import pytest
from processor.main import process_event


@pytest.fixture(scope='session')
def kinesis_event():
    """A sample Kinesis event."""
    return {
        "Records": [
            {
                "eventID": "shardId-000000000000:44200961",
                "eventVersion": "1.0",
                "kinesis": {
                    "partitionKey": "partitionKey-3",
                    "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",
                    "kinesisSchemaVersion": "1.0",
                    "sequenceNumber": "4954511524144582180062593244200961"
                    },
                "invokeIdentityArn": "arn:aws:iam::EXAMPLE",
                "eventName": "aws:kinesis:record",
                "eventSourceARN": "arn:aws:kinesis:EXAMPLE",
                "eventSource": "aws:kinesis",
                "awsRegion": "us-east-1"
                }
            ]
        }


@pytest.fixture(scope="session")
def context():
    """A dummy CF context object."""

    class DummyContext:
        def __init__(self):
            self.function_name = process_event.__name__
            self.function_version = 1
            self.invoked_function_arn = "arn"
            self.memory_limit_in_mb = 128
            self.aws_request_id = str(uuid.uuid4())
            self.log_group_name = "dummy_group"
            self.log_stream_name = "dummy_stream"
            self.identity = Mock(return_value=None)
            self.client_context = Mock(return_value=None)

        def get_remaining_Time_in_millis():
            return 100

    return DummyContext()


def test_process_event(kinesis_event, context, monkeypatch):
    """Processes a dummy event."""
    mocked_client = Mock()
    monkeypatch.setattr("boto3.client", Mock(return_value=mocked_client))
    process_event(kinesis_event, context)
    assert mocked_client.put_records.call_count == 1
