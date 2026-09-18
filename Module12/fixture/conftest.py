# Configuration Test

import logging
import pytest
from fastapi.testclient import TestClient
from main import app, items

logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    logger.info("SETUP: creating client")     # runs before each test
    with TestClient(app) as c:
        yield c
    logger.info("TEARDOWN: clearing data")     # runs after each test
    items.clear()