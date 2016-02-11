Lambda Processor
==================

This repository contains a [humilis][humilis] layer that deploys
an [AWS Lambda function][lambda] that processes events coming from an input
Kinesis stream. The processed events are then pushed to an output 
[Kinesis][kinesis] stream (that acts as a buffer for further processing).

Note that this repository is not intended to stand on its own but to be part
of a larger humilis _environment_. See [humilis][humilis] documentation for
more information.

[firehose]: http://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html
[kinesis]: https://aws.amazon.com/documentation/kinesis/
[humilis]: https://github.com/InnovativeTravel/humilis
[lambda]: https://aws.amazon.com/documentation/lambda/


## Requirements

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
