# This is where all the tests for TestingExamples.py
import unittest
import json
from src.api_service import ApiService
from datetime import date
from unittest.mock import MagicMock
from src.data_conversion_service import DataConversionService


class TestApiService(unittest.TestCase):
    def setUp(self):
        self.conversionService = DataConversionService()
        self._sut = ApiService(self.conversionService)

    def test_given_lat_lon_url_creator_returns_correct_url(self):
        lat = 10
        lon = 15
        expected = (f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude=-{lon}&hourly=temperature_2m'
                    f'&daily=weathercode,temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit'
                    f'&timezone=America%2FChicago&start_date={date.today()}&end_date={date.today()}')
        actual = self._sut.url_creator(lat, lon, date.today(), date.today())
        self.assertEqual(actual, expected)

    def test_given_lat_lon_get_todays_high_and_low_returns_good_string(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hourly': '2022'
        }
        mock_response.get.return_value = mock_response
        expected = f'The high for today will be 1.2 degrees fahrenheit and the low will be 1.0 degrees fahrenheit'
        self.conversionService.convert_json_to_high_and_low_temps_string = MagicMock(return_value=expected)
        actual = self._sut.get_todays_high_and_low(20, 20)
        self.assertEqual(actual, expected)

    def test_given_lat_lon_get_hourly_temps_returns_good_string(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hourly': '2022'
        }
        mock_response.get.return_value = mock_response
        expected = '11/24/2022 \n00:00: 1.2 degrees fahrenheit \n01:00: 1.3 degrees fahrenheit \n'
        self.conversionService.convert_temperature_dict_to_str = MagicMock(return_value=expected)
        actual = self._sut.get_hourly_temps(1, 20)
        self.assertEqual(actual, expected)

    def test_given_lat_lon_get_five_day_high_lows_returns_valid_message(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hourly': '2022'
        }
        mock_response.get.return_value = mock_response
        expected = f"Day 1: High of 15 and low of 10\n"
        self.conversionService.convert_forecast_highs_and_lows_dict_to_str = MagicMock(return_value=expected)
        actual = self._sut.get_forecasted_high_low_temps(1, 20, 1)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
