from datetime import datetime


class DataConversionService:
    @staticmethod
    def convert_json_to_high_and_low_temps_string(json):
        temperatures = json['hourly']['temperature_2m']
        highTemp = max(temperatures)
        lowTemp = min(temperatures)
        return f'The high for today will be {highTemp} degrees fahrenheit and the low will be {lowTemp} degrees fahrenheit'

    @staticmethod
    def combine_time_and_temperature_to_dictionary(json):
        times = json['hourly']['time']
        temps = json['hourly']['temperature_2m']
        combined = dict(map(lambda time, temp: (time, temp), times, temps))
        return combined

    @staticmethod
    def convert_temperature_dict_to_str(dictionary):
        # Converts the key from string to date
        date_key = datetime.strptime(list(dictionary.keys())[0], '%Y-%m-%dT%H:%M')
        # Uses converted date to prettify and adds it to the output
        res = f'{date_key.strftime("%m")}/{date_key.strftime("%d")}/{date_key.strftime("%Y")} \n'

        for key, value in dictionary.items():
            # Converts the key from string to date
            key_as_date = datetime.strptime(key, '%Y-%m-%dT%H:%M')
            time = key_as_date.strftime("%H:%M")
            res += f'{time}: {str(value)} degrees fahrenheit \n'
        return res

    @staticmethod
    def convert_forecast_high_low_json_to_dict(json):
        all_temps = json['hourly']['temperature_2m']
        all_days_with_times = json['hourly']['time']

        days = [all_days_with_times[x] for x in range(0, len(all_days_with_times), 24)]
        temps_split_by_day = [all_temps[x:x + 24] for x in range(0, len(all_temps), 24)]

        highs_and_lows_dict = {}
        print(days)
        for index, day_list in enumerate(temps_split_by_day):
            date_key = datetime.strptime(days[index], '%Y-%m-%dT%H:%M')
            date_key_formatted = f'{date_key.strftime("%m")}/{date_key.strftime("%d")}/{date_key.strftime("%Y")}'
            highs_and_lows_dict[date_key_formatted] = day_list

        return highs_and_lows_dict

    @staticmethod
    def convert_forecast_highs_and_lows_dict_to_str(dictionary):
        message = ""
        for key, value in dictionary.items():
            message += f"{key}: High of {max(value)} and low of {min(value)} \n"
        return message
