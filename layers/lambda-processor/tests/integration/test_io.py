# -*- coding: utf-8 -*-
"""
Tests the input and output Kinesis streams
"""

import pytest
import json
import time
import uuid

import boto3
from humilis.environment import Environment


@pytest.fixture(scope="session", params=[1, 10, 50, 100])
def events(request):
    """A batch of events to be ingested by Kinesis."""
    return [{
        "event_id": str(uuid.uuid4()).replace('-', ''),
        "timestamp": '2016-01-22T01:45:44.235+01:00',
        "client_id": "1628457772.1449082074",
        "url": "http://staging.findhotel.net/?lang=nl-NL",
        "referrer": "http://staging.findhotel.net/"
        } for _ in range(request.param)]


@pytest.fixture(scope="session")
def payloads(events):
    """A base 64 encoded data record."""
    payloads = []
    for kr in events:
        record = json.dumps(kr)
        payload = record
        payloads.append(payload)
    return payloads


@pytest.fixture(scope="session")
def environment(settings):
    """The lambda-processor-test humilis environment."""
    env = Environment(settings.environment_path, stage=settings.stage)
    env.create()
    return env


@pytest.fixture(scope="session")
def io_stream_names(settings, environment):
    """The name of the input and output streams in the rawpipe layer."""
    layer = [l for l in environment.layers
             if l.name == settings.io_layer_name][0]
    return (layer.outputs.get('InputStream'),
            layer.outputs.get('OutputStream'))


@pytest.fixture(scope="session")
def kinesis():
    """Boto3 kinesis client."""
    return boto3.client('kinesis')


@pytest.fixture(scope="function")
def shard_iterators(kinesis, io_stream_names):
    """Get the latest shard iterator after emptying a shard."""
    sis = []
    for stream_name in io_stream_names:
        si = kinesis.get_shard_iterator(
            StreamName=stream_name,
            ShardId='shardId-000000000000',     # Only 1 shard
            ShardIteratorType='LATEST')['ShardIterator']
        # At most 5 seconds to empty the shard
        for _ in range(10):
            kinesis_recs = kinesis.get_records(ShardIterator=si, Limit=10000)
            si = kinesis_recs['NextShardIterator']
            time.sleep(0.2)
        sis.append(si)
    return sis


def get_all_records(client, si, limit, timeout=10):
    """Retrieves all records from a Kinesis stream."""
    retrieved_recs = []
    for _ in range(timeout):
        kinesis_recs = client.get_records(ShardIterator=si, Limit=limit)
        si = kinesis_recs['NextShardIterator']
        retrieved_recs += kinesis_recs['Records']
        if len(retrieved_recs) == limit:
            # All records have been retrieved
            break
        time.sleep(1)

    return retrieved_recs


def test_io_streams_put_get_record(kinesis, io_stream_names, shard_iterators,
                                   payloads):
    """Put and read a record from the input stream."""
    input_stream, output_stream = io_stream_names

    # Latest shard iterators after emptying both the input and output streams
    input_si, output_si = shard_iterators

    # Put some records in the input stream
    response = kinesis.put_records(
        StreamName=input_stream,
        Records=[
            {
                "Data": payload,
                "PartitionKey": str(uuid.uuid4())
            } for payload in payloads])

    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    # timeout = min(max(5, 2 x (number_events), 50)
    retrieved_recs = get_all_records(kinesis, output_si, len(payloads),
                                     min(max(5, 2*len(payloads)), 50))

    assert len(retrieved_recs) == len(payloads)
    retrieved_ids = {json.loads(x['Data'].decode())['event_id'] for x
                     in retrieved_recs}
    put_ids = {json.loads(x)['event_id'] for x in payloads}
    assert not retrieved_ids.difference(put_ids)
