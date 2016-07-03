Secrets Vault
==================

[![Build Status](https://travis-ci.org/humilis/humilis-secrets-vault.svg?branch=master)](https://travis-ci.org/humilis/humilis-secrets-vault)
[![PyPI](https://img.shields.io/pypi/v/humilis-secrets-vault.svg?style=flat)](https://pypi.python.org/pypi/humilis-secrets-vault)

A [humilis][humilis] plugin that implements a `secrets-vault` layer. The layer
consists of an encrypted DynamoDB table that serves secrets to Lambda
functions in the same humilis environment. The encryption and decryption
of secrets is handled by AWS [KMS service][kms].

[humilis]: https://github.com/InnovativeTravel/humilis
[kms]: https://aws.amazon.com/kms/
[dynamodb]: https://aws.amazon.com/dynamodb/


## Installation

From [PyPI][pypi]:

[pypi]: https://pypi.python.org/pypi/humilis-secrets-vault

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
example, the environment below deploys a Lambda function that processes events
in a Kinesis stream. The Lambda processor is granted access to the secrets
vault that is also part of the same environment:

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

        - layer: event-processor
          layer_type: kinesis-processor
          dependencies: ["streams"]
          input: {layer: streams, stream: InputStream}

        - layer: secrets-vault
          layer_type: secrets-vault
          # We specify that the Lambda function in the event-processor layer
          # should have access to the secrets in the vault.
          associated_processors: ["event-processor"]
```

The `secrets-vault` layer expects that the layer(s) that contain the Lambda 
processor(s) expose a layer output `LambdaFunctionArn` with the ARN of the 
Lambda function that should have access to the secrets in the vault. Layers
of type [kinesis-processor][kinesis-processor] as in the example above
fulfil this expectation so they will work out-of-the-box.

[kinesis-processor]: https://github.com/humilis/humilis-kinesis-processor


### Retrieving secrets

The easiest way of retrieving secrets from your Lambda function is to include
package [lambdautils][lambdautils] as a depencency.

[lambdautils]: https://github.com/humilis/humilis-lambdautils

Then you can easily retrieve secrets from the vault within your Lambda code as
follows:

```
import lambdautils.utils as utils

# Assuming that you are deploying this Lambda with humilis the line below
# will indicate humilis to preprocess this function with Jinja2 before
# producing the Lambda deployment package.
# preprocessor:jinja2

# During deployment, humilis will replace here the name of the humilis
# environment and deployment stage.
ENVIRONMENT = "{{_env.name}}"
STAGE = "{{_env.stage}}"

plaintext = utils.get_secret(
    "my_secret_key", environment=ENVIRONMENT, stage=STAGE)

```


### Storing secrets

You can use [humilis][humilis] to store secrets in the vault from the command
line:

```
humilis set-secret --stage [STAGE] [ENVIRONMENT_FILE] [SECRET_KEY] [SECRET_VALUE]
```


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


## Contact

If you have questions, bug reports, suggestions, etc. please create an issue on
the [GitHub project page][github].

[github]: http://github.com/humilis/humilis-secrets-vault


## License

This software is licensed under the [MIT license][mit].

[mit]: http://en.wikipedia.org/wiki/MIT_License

See [License file][LICENSE].

[LICENSE]: https://github.com/humilis/humilis-secrets-vault/blob/master/LICENSE.txt


© 2016 German Gomez-Herrero, [Find Hotel][fh] and others.

[it]: http://company.findhotel.net
