import os
import tempfile
import pytest

from api import app

@pytest.fixture
def client():

    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_index_get(client):

    response = client.get('/')

    assert response.status_code == 200
    assert response.json['greeting'] == 'Hello, DevGrid!'


def test_weather_list_empty_get(client):

    response = client.get('/weather')

    assert response.status_code == 404
    assert response.json['message'] == 'Weather list not found'


def test_weather_get(client):

    response = client.get('/weather/Sao Paulo') # without accents

    assert response.status_code == 200
    assert response.json['city'] == 'São Paulo'
    assert type(response.json['temp']) == float
    assert type(response.json['weather']) == str

    response = client.get('weather/london') # with lowercase letters

    assert response.status_code == 200
    assert response.json['city'] == 'London'
    assert type(response.json['temp']) == float
    assert type(response.json['weather']) == str

    response = client.get('weather/lonfoodonbar') # with wrong city name

    assert response.status_code == 404
    assert response.json['message'] == 'Weather not found'


def test_weather_list_get(client):

    client.get('/weather/Toronto')
    client.get('/weather/Amsterdam')
    client.get('/weather/Berlin')
    client.get('/weather/Oslo')

    response = client.get('/weather')

    assert response.status_code == 200
    assert len(response.json) == 5
    assert response.json[0]['city'] == 'Oslo'
    assert response.json[4]['city'] == 'London'

    response = client.get('/weather?max=3')

    assert len(response.json) == 3


def test_weather_list_with_invalid_params_get(client):

    response = client.get('/weather?max=-3')

    assert response.status_code == 400
    assert response.json['message'] == 'The \'max\' attribute must be a positive integer between 1 and 5. Example: 4'

    response = client.get('/weather?max=0')

    assert response.status_code == 400
    assert response.json['message'] == 'The \'max\' attribute must be a positive integer between 1 and 5. Example: 4'

    response = client.get('/weather?max=6')

    assert response.status_code == 400
    assert response.json['message'] == 'The \'max\' attribute must be a positive integer between 1 and 5. Example: 4'

    response = client.get('/weather?max=foo')

    assert response.status_code == 400
    assert response.json['message'] == 'The \'max\' attribute must be a positive integer between 1 and 5. Example: 4'
