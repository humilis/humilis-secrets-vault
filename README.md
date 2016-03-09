Secrets Vault
==================

[![PyPI](https://img.shields.io/pypi/v/humilis-filter.svg?style=flat)](https://pypi.python.org/pypi/humilis-secrets-vault)

A [humilis][humilis] plugin that deploys an encrypted DynamoDB table that
serves secrets to one or more Lambda functions. The encryption and decryption
of secrets is handled by AWS [KMS service][kms].

[humilis]: https://github.com/InnovativeTravel/humilis
[kms]: https://aws.amazon.com/kms/
[dynamodb]: https://aws.amazon.com/dynamodb/


## Installation

From [PyPI][pypi]:

```
pip install humilis-secrets-vault
```

To install the dev version:

```
pip install git+https://github.com/InnovativeTravel/humilis-secrets-vault
```


## How do I use this?

Simply add this layer to your [humilis][humilis] environment and use the
layer parameter `associated_processors` to specify the layers that contain
the Lambda functions that require access to the secrets in the vault. For
example, the environment below deploys a Lambda function that filters events
in a Kinesis stream and gives the Lambda access to the secrets vault that is 
also part of the same environment:

```
---
myenvironment:
    description:
        An environment with a Lambda processor to filter events in a Kinesis
        stream.

    layers:
        - layer: streams
          layer_type: streams
          streams:
              - name: InputStream
                shard_count: 1
              - name: OutputStream
                shard_count: 1
              - name: MatchedStream
                shard_count: 1

        - layer: filter
          layer_type: filter
          dependencies: ["streams"]
          input: {layer: streams, stream: InputStream}
          output: {layer: streams, stream: OutputStream}
          # Do not delivered the unmatched events anywhere
          matched: {layer: streams, stream: MatchedStream}
          input_delivery: False
          output_delivery: False
          matched_delivery: False

        - layer: secrets-vault
          layer_type: secrets-vault
          # We specify that the Lambda processor in the filter layer should
          # have access to the secrets in the vault.
          associated_processors: ["filter"]
```



### Retrieving secrets 

To be able to retrieve secrets your Lambda function should include
package [lambdautils][lambdautils] as a depencency.

[lambdautils]: https://github.com/InnovativeTravel/humilis-lambdautils

Then you can easily retrieve secrets from the vault within your Lambda code as
follows:

```
import lambdautils.utils as utils

plaintext = utils.get_secret("key_for_my_secret")

```


### Storing secrets

You can use [humilis][humilis] to store secrets in the vault from the command
line:

```
humilis set-secret --stage [STAGE] [ENVIRONMENT_FILE] [SECRET_ID] [SECRET_VALUE]
```


## Deployment requirements

You need to install [humilis][humilis] and configure a local profile:

```
humilis configure --local
```

The command above will create a `.humilis.ini` file that you can keep with the
rest of your code. This repository contains one such file with values that make
sense for people working at Innovative Travel.


## Development

Assuming you have [virtualenv][venv] installed:

[venv]: https://virtualenv.readthedocs.org/en/latest/

```
make develop
```

Configure humilis:

```
.env/bin/humilis configure --local
```


## Testing

You can test the deployment of the secrets vault using:

```bash
make create
```

Then you can then run the integration test suite (TBD):

```
make testi
```

Don't forget to delete the test deployment once you are done:

```bash
make delete
```


## More information

See [humilis][humilis] documentation.

[humilis]: https://github.com/InnovativeTravel/humilis/blob/master/README.md


## Who do I ask?

Ask [German](mailto:german@innovativetravel.eu).
