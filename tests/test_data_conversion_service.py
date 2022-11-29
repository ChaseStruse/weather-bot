import unittest
import json

from src.data_conversion_service import DataConversionService


class TestApiService(unittest.TestCase):
    def setUp(self):
        self._sut = DataConversionService()

    def test_given_json_convert_json_to_high_and_low_temps_string_returns_correct_string(self):
        given = '{ "hourly": { "temperature_2m": [1.2, 1.3, 1.4, 1.5] } }'
        expected = f'The high for today will be 1.5 degrees fahrenheit and the low will be 1.2 degrees fahrenheit'
        actual = self._sut.convert_json_to_high_and_low_temps_string(json.loads(given))
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
        actual = self._sut.combine_time_and_temperature_to_dictionary(json.loads(given))
        self.assertEqual(actual, expected)

    def test_given_dictionary_convert_dict_to_str_returns_correct_string(self):
        given = {
            "2022-11-24T00:00": 1.2,
            "2022-11-24T01:00": 1.3
        }
        expected = '11/24/2022 \n00:00: 1.2 degrees fahrenheit \n01:00: 1.3 degrees fahrenheit \n'
        actual = self._sut.convert_temperature_dict_to_str(given)
        self.assertEqual(actual, expected)

    def test_given_valid_json_convert_five_day_json_to_dict_returns_valid_dict(self):
        given = ('{ "hourly": { "temperature_2m": [1.2, 1.3, 1.4, 1.5, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 1, 2, 3, '
                 '4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 10, 2, 3, 4, 5, 1, 1, 1, 2, 3, 4, 10, 11, 1, 1, 1, '
                 '4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 1, 2, 3, 4, 5, 60, 1, 2, 3, 4, 5, 1, 1, 1, 2, 3, 4, 10, 11, 1, 1, '
                 '1, 1, 3, 4, 5, 2, 1, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2, 1, 3, '
                 '4, 1, 2, 1, 2, 1, 2] } } ')
        expected = {
            "1": [1.2, 1.3, 1.4, 1.5, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8],
            "2": [9, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 10, 2, 3, 4, 5, 1, 1, 1, 2, 3, 4, 10, 11],
            "3": [1, 1, 1, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 1, 2, 3, 4, 5, 60, 1, 2, 3, 4, 5],
            "4": [1, 1, 1, 2, 3, 4, 10, 11, 1, 1, 1, 1, 3, 4, 5, 2, 1, 9, 1, 2, 3, 4, 5, 6],
            "5": [7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2, 1, 3, 4, 1, 2, 1, 2, 1, 2]
        }
        actual = self._sut.convert_five_day_json_to_dict(json.loads(given))
        self.assertEqual(actual, expected)

    def test_given_valid_dict_convert_five_day_highs_and_lows_dict_to_str_returns_correct_message(self):
        given = {
            "1": [1.2, 1.3, 1.4, 1.5, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8],
            "2": [9, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 10, 2, 3, 4, 5, 1, 1, 1, 2, 3, 4, 10, 11],
            "3": [1, 1, 1, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 1, 2, 3, 4, 5, 60, 1, 2, 3, 4, 5],
            "4": [1, 1, 1, 2, 3, 4, 10, 11, 1, 1, 1, 1, 3, 4, 5, 2, 1, 9, 1, 2, 3, 4, 5, 6],
            "5": [7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2, 1, 3, 4, 1, 2, 1, 2, 1, 2]
        }
        expected = (f"Day 1: High of {max(given['1'])} and low of {min(given['1'])} \n"
                    f"Day 2: High of {max(given['2'])} and low of {min(given['2'])} \n"
                    f"Day 3: High of {max(given['3'])} and low of {min(given['3'])} \n"
                    f"Day 4: High of {max(given['4'])} and low of {min(given['4'])} \n"
                    f"Day 5: High of {max(given['5'])} and low of {min(given['5'])} \n")
        actual = self._sut.convert_five_day_highs_and_lows_dict_to_str(given)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
