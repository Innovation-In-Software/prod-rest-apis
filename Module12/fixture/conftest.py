# Configuration Test

import logging
import pytest
from fastapi.testclient import TestClient
from main import app, items

logging.basicConfig(filename="test.log", level=logging.INFO)

@pytest.fixture
def client():
    logging.info("SETUP: creating client")     # runs before each test
    with TestClient(app) as c:
        yield c                                # yield runs the unit test
    logging.info("TEARDOWN: clearing data")     # runs after each test
    items.clear()