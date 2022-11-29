import os
import discord
from dotenv import load_dotenv
from api_service import ApiService
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
    long = location.longitude
    return lat, long


@bot.command(name='weather_hourly')
async def weather_hourly(ctx, *args):
    try:
        location_name = ' '.join(args)
        print(location_name)
        lat, lon = get_latitude_longitude(location_name)
        res = api_service.get_hourly_temps(lat, lon)
        await ctx.send(f'`{res}`')
    except:
        await ctx.send('Please ensure you have added City StateAbbreviation')


@bot.command(name='weather_highlow')
async def weather_high_low_temps(ctx, *args):
    try:
        location_name = ' '.join(args)
        lat, lon = get_latitude_longitude(location_name)
        res = api_service.get_todays_high_and_low(lat, lon)
        await ctx.send(f'`{res}`')
    except:
        await ctx.send('Please ensure you have added City StateAbbreviation')


@bot.command(name='weather_5dayhighlow')
async def weather_five_day_high_low_temps(ctx, *args):
    try:
        location_name = ' '.join(args)
        lat, lon = get_latitude_longitude(location_name)
        res = api_service.get_five_day_highs_and_lows(lat, lon)
        await ctx.send(f'`{res}`')
    except:
        await ctx.send('Please ensure you have added City StateAbbreviation')


@bot.command(name='weather_help')
async def weather_help(ctx):
    await ctx.send('List of Commands: \n '
                   '`!weather_hourly` City StateAbbreviation \n '
                   'ex: `!weather_hourly` Des Moines IA \n'
                   '\n'
                   '`!weather_highlow` City StateAbbreviation \n'
                   'ex: `!weather_highlow` Des Moines IA \n'
                   '\n'
                   '`!weather_5dayhighlow` City StateAbbreviation \n'
                   'ex: `!weather_5dayhighlow` Des Moines IA \n'
                   )


bot.run(TOKEN)
