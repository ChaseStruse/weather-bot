import os
import discord
from dotenv import load_dotenv
from src.services.api_service import ApiService
from geopy.geocoders import Nominatim
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix="!", intents=discord.Intents.all())
api_service = ApiService()


def get_latitude_longitude(location_name):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(location_name)
    lat = location.latitude
    lon = location.longitude
    return lat, lon


@bot.command(name='hourlytemps')
async def hourly_temperatures(ctx, *args):
    try:
        location_name = ' '.join(args)
        print(location_name)
        lat, lon = get_latitude_longitude(location_name)
        res = api_service.get_hourly_temps(lat, lon)
        await ctx.send(f'`{res}`')
    except AttributeError:
        await ctx.send('Please ensure you have added City StateAbbreviation')


@bot.command(name='todayshighlow')
async def high_low_temps(ctx, *args):
    try:
        location_name = ' '.join(args)
        lat, lon = get_latitude_longitude(location_name)
        res = api_service.get_todays_high_and_low(lat, lon)
        await ctx.send(f'`{res}`')
    except AttributeError:
        await ctx.send('Please ensure you have added City StateAbbreviation')


@bot.command(name='highlowforecast')
async def forecast_high_low_temps(ctx, *args):
    try:
        number_of_days = int(args[-1])
        if number_of_days > 10:
            raise ValueError

        args = args[:-1]
        location_name = ' '.join(args)
        lat, lon = get_latitude_longitude(location_name)
        res = api_service.get_forecasted_high_low_temps(lat, lon, number_of_days)
        await ctx.send(f'`{res}`')

    except AttributeError:
        await ctx.send('Please ensure you have added City StateAbbreviation')
    except ValueError:
        await ctx.send('Forecast must be less than or equal to 10 days please')


@bot.command(name='weather_help')
async def weather_help(ctx):
    await ctx.send('List of Commands: \n '
                   '`!hourlytemps` City StateAbbreviation \n '
                   'ex: `!hourlytemps` Des Moines IA \n'
                   '\n'
                   '`!todayshighlow` City StateAbbreviation \n'
                   'ex: `!todayshighlow` Des Moines IA \n'
                   '\n'
                   '`!highlowforecast` City StateAbbreviation NumberOfDays (must be less than or equal to 10 days)\n'
                   'ex: `!highlowforecast` Des Moines IA 10\n'
                   )


bot.run(TOKEN)
