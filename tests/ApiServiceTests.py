# This is where all the tests for TestingExamples.py
import unittest
import json

import requests

from ApiService import ApiService
from datetime import date
from unittest.mock import MagicMock


class TestApiService(unittest.TestCase):
    def setUp(self):
        self.apiService = ApiService()

    def test_given_lat_lon_url_creator_returns_correct_url(self):
        lat = 10
        lon = 15
        expected = (f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude=-{lon}&hourly=temperature_2m'
                    f'&daily=weathercode,temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit'
                    f'&timezone=America%2FChicago&start_date={date.today()}&end_date={date.today()}')
        actual = self.apiService.url_creator(lat, lon)
        self.assertEqual(actual, expected)

    def test_given_json_convert_json_to_high_and_low_temps_string_returns_correct_string(self):
        given = '{ "hourly": { "temperature_2m": [1.2, 1.3, 1.4, 1.5] } }'
        expected = f'The high for today will be 1.5 degrees fahrenheit and the low will be 1.2 degrees fahrenheit'
        actual = self.apiService.convert_json_to_high_and_low_temps_string(json.loads(given))
        self.assertEqual(actual, expected)

    def test_given_json_combine_time_and_temperature_to_dictionary_returns_correct_dictionary(self):
        given = '{ "hourly": { "time":["2022-11-24T00:00", "2022-11-24T01:00", "2022-11-24T02:00", ' \
                '"2022-11-24T03:00"], "temperature_2m": [1.2, 1.3, 1.4, 1.5] } } '
        expected = {
            "2022-11-24T00:00": 1.2,
            "2022-11-24T01:00": 1.3,
            "2022-11-24T02:00": 1.4,
            "2022-11-24T03:00": 1.5
        }
        actual = self.apiService.combine_time_and_temperature_to_dictionary(json.loads(given))
        self.assertEqual(actual, expected)

    def test_given_dictionary_convert_dict_to_str_returns_correct_string(self):
        given = {
            "2022-11-24T00:00": 1.2,
            "2022-11-24T01:00": 1.3
        }
        expected = '11/24/2022 \n00:00: 1.2 degrees fahrenheit \n01:00: 1.3 degrees fahrenheit \n'
        actual = self.apiService.convert_dict_to_str(given)
        self.assertEqual(actual, expected)

    def test_given_lat_lon_get_todays_high_and_low_returns_good_string(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hourly': '2022'
        }
        mock_response.get.return_value = mock_response
        expected = f'The high for today will be 1.2 degrees fahrenheit and the low will be 1.0 degrees fahrenheit'
        self.apiService.convert_json_to_high_and_low_temps_string = MagicMock(return_value=expected)
        actual = self.apiService.get_todays_high_and_low(20, 20)
        self.assertEqual(actual, expected)

    def test_given_lat_lon_get_hourly_temps_returns_good_string(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hourly': '2022'
        }
        mock_response.get.return_value = mock_response
        expected = '11/24/2022 \n00:00: 1.2 degrees fahrenheit \n01:00: 1.3 degrees fahrenheit \n'
        self.apiService.convert_dict_to_str = MagicMock(return_value=expected)
        actual = self.apiService.get_hourly_temps(1, 20)
        self.assertEqual(actual, expected)