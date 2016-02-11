from processor.main import process_event


def lambda_handler(event, context):
    return process_event(event, context)
