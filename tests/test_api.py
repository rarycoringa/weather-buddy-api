import os
import pytest
import time

from api import app

class TestIndexResource:

    def test_index_get(self, client):

        # Act
        response = client.get('/')

        # Assert
        assert response.status_code == 200
        assert response.json['greeting'] == 'Hello, DevGrid!'


class TestWeatherResource:

    def test_weather_get(self, client):

        # Act
        response = client.get('/weather/London')

        # Assert
        assert response.status_code == 200
        assert response.json['city']['name'] == 'London'
        assert response.json['city']['country'] == 'GB'
        assert type(response.json['city']['coordinates']) == list


    def test_weather_not_found(self, client):

        # Act
        response = client.get('/weather/LondonFooBar')

        # Assert
        assert response.status_code == 404
        assert response.json['message'] == 'Weather not found'


class TestWeatherListResource:

    def test_weather_list_get(self, client):

        # Act
        client.get('/weather/London')
        client.get('/weather/Manchester')

        response = client.get('/weather')

        # Assert
        assert response.status_code == 200
        assert type(response.json) == list
        assert len(response.json) == 2


    def test_weather_list_empty_get(self, client):

        # Act
        response = client.get('/weather')

        # Assert
        assert response.status_code == 404
        assert response.json['message'] == 'Weather list not found'


    def test_weather_list_with_invalid_params_get(self, client):

        # Act
        response_list = []
        response_list.append(client.get('/weather?max=-3'))
        response_list.append(client.get('/weather?max=0'))
        response_list.append(client.get('/weather?max=6'))
        response_list.append(client.get('/weather?max=foo'))

        # Assert
        for response in response_list:
            assert response.status_code == 400
            assert response.json['message'] == 'The \'max\' attribute must be a positive integer between 1 and 5. Example: 4'
