"""Global conftest."""
import pytest
from collections import namedtuple


@pytest.fixture(scope="session")
def settings():
    """Global test settings."""
    Settings = namedtuple('Settings', 'stage environment_path io_layer_name')
    return Settings(stage="TEST",
                    environment_path="lambda-processor-test.yaml",
                    io_layer_name="io-streams")
