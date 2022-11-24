import os
import discord
from dotenv import load_dotenv
from ApiService import ApiService
from geopy.geocoders import Nominatim

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.all())
api_service = ApiService()


def get_latitude_longitude(location_name):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(location_name)
    lat = location.latitude
    long = location.longitude
    return lat, long


@client.event
async def on_ready():
    try:
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print('Successfully connected')
    except:
        print('Exception when connecting')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:15] == '!weather hourly':
        try:
            location_name = message.content[16:]
            lat, lon = get_latitude_longitude(location_name)
            res = api_service.get_hourly_temps(lat, lon)
            await message.channel.send(f'`{res}`')
        except:
            await message.channel.send('Please ensure you have added City StateAbbreviation')

    elif message.content[0:16] == '!weather highlow':
        try:
            location_name = message.content[17:]
            lat, lon = get_latitude_longitude(location_name)
            res = api_service.get_todays_high_and_low(lat, lon)
            await message.channel.send(f'`{res}`')
        except:
            await message.channel.send('Please ensure you have added City StateAbbreviation')

    elif message.content == '!weather help':
        await message.channel.send('List of Commands: \n '
                                   '!weather hourly City StateAbbreviation \n '
                                   'ex: !weather hourly Des Moines IA \n'
                                   '\n'
                                   '!weather highlow City StateAbbreviation \n'
                                   'ex: !weather highlow Des Moines IA \n')


client.run(TOKEN)
