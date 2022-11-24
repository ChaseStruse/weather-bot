import requests
from datetime import date, datetime


class ApiService:
    def __init__(self):
        self.defaultUrl = 'https://api.open-meteo.com/v1/forecast?'
        self.todaysDate = date.today()

    def url_creator(self, lat, lon):
        url = (f'{self.defaultUrl}latitude={lat}&longitude=-{lon}&hourly=temperature_2m'
               f'&daily=weathercode,temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit'
               f'&timezone=America%2FChicago&start_date={self.todaysDate}&end_date={self.todaysDate}')
        return url

    def get_todays_high_and_low(self, lat, lon):
        response = requests.get(self.url_creator(lat, abs(lon)))
        return self.high_and_low_temps(response.json())

    def get_hourly_temps(self, lat, lon):
        response = requests.get(self.url_creator(lat, abs(lon)))
        return self.convert_dict_to_str(self.hourly_temps(response.json()))

    @staticmethod
    def high_and_low_temps(json):
        temperatures = json['hourly']['temperature_2m']
        highTemp = max(temperatures)
        lowTemp = min(temperatures)
        return f'The high for today will be {highTemp} degrees fahrenheit and the low will be {lowTemp} degrees fahrenheit'

    @staticmethod
    def hourly_temps(json):
        times = json['hourly']['time']
        temps = json['hourly']['temperature_2m']
        combined = dict(map(lambda time, temp: (time, temp), times, temps))
        return combined

    @staticmethod
    def convert_dict_to_str(dictionary):
        # Converts the key from string to date
        date_key = datetime.strptime(list(dictionary.keys())[0], '%Y-%m-%dT%H:%M')
        # Uses converted date to prettify and adds it to the output
        res = f'{date_key.strftime("%m")}/{date_key.strftime("%d")}/{date_key.strftime("%Y")} \n'

        for key, value in dictionary.items():
            # Converts the key from string to date
            key_as_date = datetime.strptime(key, '%Y-%m-%dT%H:%M')
            time = key_as_date.strftime("%H:%M:%S")
            res += f'{time}: {str(value)} degrees fahrenheit \n'
        return res
