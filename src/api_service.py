import requests
from datetime import timedelta, date
from src.data_conversion_service import DataConversionService


class ApiService:
    def __init__(self, _data_conversion_service=DataConversionService()):
        self.defaultUrl = 'https://api.open-meteo.com/v1/forecast?'
        self.todaysDate = date.today()
        self.conversionService = _data_conversion_service

    def url_creator(self, lat, lon, start_date, end_date):
        url = (f'{self.defaultUrl}latitude={lat}&longitude=-{lon}&hourly=temperature_2m'
               f'&daily=weathercode,temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit'
               f'&timezone=America%2FChicago&start_date={start_date}&end_date={end_date}')
        return url

    def get_todays_high_and_low(self, lat, lon):
        response = requests.get(self.url_creator(lat, abs(lon), self.todaysDate, self.todaysDate))
        return self.conversionService.convert_json_to_high_and_low_temps_string(response.json())

    def get_hourly_temps(self, lat, lon):
        response = requests.get(self.url_creator(lat, abs(lon), self.todaysDate, self.todaysDate))
        temperature_dict = self.conversionService.combine_time_and_temperature_to_dictionary(response.json())
        return self.conversionService.convert_temperature_dict_to_str(temperature_dict)

    def get_five_day_highs_and_lows(self, lat, lon):
        end_date = self.todaysDate + timedelta(days=4)
        response = requests.get(self.url_creator(lat, abs(lon), self.todaysDate, end_date))
        high_and_low_dict = self.conversionService.convert_five_day_json_to_dict(response.json())
        return self.conversionService.convert_five_day_highs_and_lows_dict_to_str(high_and_low_dict)
