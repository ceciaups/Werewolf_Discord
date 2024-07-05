import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

BOT_PREFIX = '!'

@client.event
async def on_ready():
  for guild in client.guilds:
        if guild.name == GUILD:
            break

  print(
    f'{client.user} has connected to Discord!\n'
  )

@client.event
async def on_message(message):
  if message.content.strip().startswith(BOT_PREFIX):
    command = message.content.strip()[len(BOT_PREFIX):].lower().split(' ')[0]
    parameters = message.content.strip().lower().split(' ')[1:]

client.run(TOKEN)