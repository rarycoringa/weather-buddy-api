import os
import pytest

from api import app, cache

#Arrange
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        cache.clear()
