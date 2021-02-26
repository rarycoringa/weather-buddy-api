from flask_restful import Resource, reqparse

class WeatherCityListView(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            'max',
            type=int,
            help='The \'max\' attribute must be a positive integer. Example: 4.'
        )

        args = parser.parse_args(strict=True)

        max_number = args['max'] if args['max'] is not None else 5

        cities = [{'name': 'Floripa'}, {'name': 'Natal'}]
        return {'cities': cities}

class WeatherCityView(Resource):
    def get(self, city_name):
        return {'city': city_name}
