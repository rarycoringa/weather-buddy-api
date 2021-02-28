# Weather Buddy API

<img align="right" width="120" src="img/devgrid.png">

![GitHub release](https://img.shields.io/github/v/release/rarygc/weather-buddy-api?include_prereleases)
![GitHub license](https://img.shields.io/github/license/rarygc/weather-buddy-api)

## About this application

An Rest API to perform weather requests with the OpenWeatherMap API, developed with the objective of fix the need raised by the initial challenge of the selection process for back-end developer of **[DevGrid](https://devgrid.co.uk)**.

## Run the application with Docker

To run this project in a simple way, it's necessary that you have **Docker** in the version >= 19 and **Docker Compose** in the version >= 1.25 installed on your machine.

1. First, clone the remote application repository on your local machine:

 ```bash
 $ git clone https://github.com/rarygc/weather-buddy-api.git
 ```

2. Then, access the application's base directory:

 ```bash
 $ cd weather-buddy-api
 ```

3. Finally, being in the directory, just build and up a container with the application in Flask:

 ```bash
 $ docker-compose up --build
 ```

**Ready!** The Rest API is available on your local machine on the URL `http://localhost:5000/`

## Services available in the application

As requested by the initial challenge, the application consists of a set of microservices for to perform weather requests with the OpenWeatherMap API in JSON format.

The application provides a service interface mapped below:

### Index

It's a small initial interface that returns a message of greetings. If you can see it **"Hello, DevGrid!"**, it means that the application is fully operational.

**GET** `http://localhost:5000/` *Get the main page greeting*

- **Parameters**

  This endpoint has no input parameters.

- **Response**

  This is the result for `http://localhost:5000`:

  ```json
  {
    "greeting": "Hello, DevGrid!"
  }
  ```

### Weather

It's the main interface of the application. It's responsible for providing the Weather management functionality. From this interface, we can request the weather in cities.

**GET** `http://localhost:5000/weather/{city_name}` *get a city weather*

- **Parameters**

  This endpoint has no input parameters.

- **Responses**
  This is the result for `http://localhost:5000/weather/Florianópolis`:

  ```json
  {
    "city": "Florianópolis",
    "temp": 26.02,
    "weather": "Scattered Clouds"
  }
  ```
  > Once requested, this city will be available for 5 minutes in cache.

**GET** `http://localhost:5000/weather` *get a list of weathers in cache*

- **Parameters**

  |key|description|type|required|
  |-|-|-|-|
  |`max`|Define the number of cities to be request. This parameter must be a positive integer between 1 and 5. Ex.: `4`. If not informed, the default value will be `5`|integer|**no**|

- **Responses**
  This is the result for `http://localhost:5000/weather` with `max = 4`:

  ```json
  [
    {
      "city": "São Paulo",
      "temp": 19.66,
      "weather": "Light Rain"
    },
    {
      "city": "Porto Alegre",
      "temp": 24.28,
      "weather": "Clear Sky"
    },
    {
      "city": "Belo Horizonte",
      "temp": 21,
      "weather": "Clear Sky"
    },
    {
      "city": "Florianópolis",
      "temp": 25.4,
      "weather": "Scattered Clouds"
    }
  ]
  ```
