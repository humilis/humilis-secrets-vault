# -*- coding: utf-8 -*-
from __future__ import print_function

# Tell humilis to pre-process the file using Jinja2
# preprocessor:jinja2

import base64
import json
import uuid

import boto3

# Jinja2 will inject here the name of the delivery stream (see meta.yaml)
# For local testing you obviously need to mock firehose.put_record()
OUTPUT_STREAM_NAME = "{{output_stream.name}}"


def process_event(event, context):
    """Forwards events to a Kinesis stream (for further processing) and
    to a Kinesis Firehose delivery stream (for persistence in S3 and/or
    Redshift)"""
    print("Received event: " + json.dumps(event, indent=2))

    resp = send_to_output_stream(event)
    print(resp)
    return 'Successfully processed {} records: {}'.format(
        len(event['Records']), resp)


def send_to_output_stream(event):
    """Sends events to the output Kinesis stream for further processing."""
    kinesis = boto3.client('kinesis')
    print("Putting records in output stream '{}'".format(OUTPUT_STREAM_NAME))
    kinesis_records = make_kinesis_records(event['Records'])
    print("Records put be sent to kinesis:")
    print(kinesis_records)
    resp = kinesis.put_records(
        StreamName=OUTPUT_STREAM_NAME,
        Records=kinesis_records)
    return resp


def make_kinesis_records(records):
    """Creates Kinesis records."""
    krs = []
    for record in records:
        kinesis_record = {
            'Data': base64.decodestring(record['kinesis']['data']),
            'PartitionKey': str(uuid.uuid4())}
        krs.append(kinesis_record)
    return krs
