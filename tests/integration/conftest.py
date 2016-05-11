"""Fixtures for the integration tests suite."""
import pytest

from humilis.environment import Environment


@pytest.yield_fixture(scope="module")
def environment():
    """The test environment: this fixtures creates it and takes care of
    removing it after tests have run."""
    env = Environment("tests/integration/secrets-vault.yaml")
    env.create()
    yield env
    env.delete()
