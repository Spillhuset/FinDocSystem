__version__='0.0.1'
__author__='Danielfiks'
__doc__ = '''The purpose of this bot is to gather invoice info from the user 
and generate a json file.'''

import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

description = """A bot for creating finance documentation"""

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


TOKEN =  os.getenv('DISCORD_TOKEN')
channelID = os.getenv('DISCORD_CHANNEL_ID')

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# client = discord.Client(intents=intents)
channel = bot.get_channel(int(channelID))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await channel.send(f'We have logged in as {bot.user}')
    await channel.send(discord.Object(id=channelID))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Section for creating discord menu.
# Model View Controller maybe



def main():
    # client.run(TOKEN, log_handler=handler)
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)


if __name__ == '__main__':
    main()

