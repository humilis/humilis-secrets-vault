# The integration tests require Python 3.x (because of humilis) while the local
# test suite should use Python 2.x because that the environment for AWS Lambda
# functions.
PIP := .env/bin/pip
TOX := .env/bin/tox
PIPI := .envi/bin/pip
TOXI := .envi/bin/tox
STAGE := TEST
HUMILIS_ENV := lambda-processor-test

# create a python2.7 virtualenv for development and local testing
.env:
	virtualenv .env -p python2.7

# create a python3 virtualenv for running integration tests
.envi:
	virtualenv .envi -p python3

# create symlinks
symlinks:
	rm -f layers/lambda-processor
	ln -fs ../ layers/lambda-processor

# set up development environment
develop: .env .envi symlinks
	$(PIP) install -r requirements-dev.txt
	$(PIPI) install -r requirements-dev.txt
	mkdir -p layers

# run local test suite
test: develop
	$(TOX) -e local

# run integration test suite
testi: develop
	$(TOXI) -e integration

# remove virtualenv and layers dir
clean:
	rm -rf .env .envi .tox .toxi
	rm layers/lambda-processor

# make a test deployment in AWS from scratch
create:
	humilis create \
	  --stage $(STAGE) \
	  --output $(HUMILIS_ENV)-$(STAGE).outputs.yaml $(HUMILIS_ENV).yaml

update:
	humilis update --stage $(STAGE) $(HUMILIS_ENV).yaml


delete:
	humilis delete --stage $(STAGE) $(HUMILIS_ENV).yaml
