Secrets Vault
==================

A [humilis][humilis] plugin that deploys an encrypted DynamoDB table that
serves secrets to one or more Lambda functions. The encryption and decryption
of secrets is handled by AWS [KMS service][kms].

[humilis]: https://github.com/InnovativeTravel/humilis
[kms]: https://aws.amazon.com/kms/
[dynamodb]: https://aws.amazon.com/dynamodb/


## How do I use this?


### Retrieving secrets 

Once this layer is deployed you should be able to retrieve secrets from the
associated Lambda processors as follows:

```python
import boto3

TABLE_NAME = "secrets_{{_env.name}}_{{_env.stage}}"

# Retrieve from DynamoDB. It assumes that the DynamoDB table has two columns:
# * id: The primary key identifying your secrets
# * value: The encrypted value of your secret
client = boto3.client('dynamodb')
encrypted = client.get_item(
    TableName=TABLE_NAME,
    Key={'id': {'S': 'mysecret'}})['Item']['value']['B']

# Decrypt using KMS (assuming the secret value is a string)
client = boto3.client('kms')
plaintext = client.decrypt(CiphertextBlob=encrypted)['Plaintext'].decode()
```


### Storing secrets

```python
KMS_KEY_ID = 'your_kms_key_id_here' # Retrieve from the deployment outputs
MY_SECRET = 'plaintext_secret'
MY_SECRET_ID = 'topsecret'
TABLE_NAME = "secrets_{{_env.name}}_{{_env.stage}}"

# Encrypt using KMS
encrypted_secret = kms.encrypt(
    KeyId=KMS_KEY_ID, 
    Plaintext=MY_SECRET)['CiphertextBlob']

# Store in DynamoDB
client = boto3.client('dynamodb')
client.put_item(
    TableName=TABLE_NAME, 
    Item={'id': {'S': MY_SECRET_ID}, 'value': {'B': encrypted_secret}})
```

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


## Testing

To run the local test suite:

```
make test
```


## Development

Assuming you have [virtualenv][virtualenv] installed:

[virtualenv]: https://virtualenv.readthedocs.org/en/latest/

```
make develop
```


## Testing

To run the local test suite (does not require deployment):

```
make test
```

To run the integration test suite, which requires deployment:

```
make testi
```


## Deployment

```
make create 
```

This will deploy to a _humilis_ stage called `TEST`. You can decide
to deploy on a different stage (e.g. `DEV`) by running:

```
make STAGE=DEV create
```

Note however that the integration test suite expects a deployment in a
`TEST` stage.

Remember to delete the deployment when you are done with testing:

```
make delete
```

Alternatively you can just run `make clean` to delete the deployment and the
development virtualenv.

To deploy updates to an existing deployment run:

```
make update
```


## More information

See [humilis][humilis] documentation.


## Who do I ask?

Ask [German](mailto:german@innovativetravel.eu)
