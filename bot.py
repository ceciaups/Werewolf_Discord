import os

import random
import re

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
# CHANNEL = os.getenv('DISCORD_CHANNEL')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Class
class Settings:
  def __init__(self, config, number, players):
    self.config = config
    self.number = number
    self.players = players

class Player:
  def __init__(self, memberId, number, role):
    self.memberId = memberId
    self.number = number
    self.role = role

# global settings variables
roles = ""
settings = Settings([], 0, [])

@bot.event
async def on_ready():
  # for guild in client.guilds:
  #       if guild.name == GUILD:
  #           break
  print(
    f'{bot.user} has connected to Discord!\n'
  )

@bot.command(name='start')
async def _start(ctx: commands.Context):
  await ctx.send('** \'!exit\'可以隨時離開遊戲！ **')

  # CONFIGURE THE GAME: PLAYERS
  members = ctx.channel.members
  # remove bot and admin
  indexes = []
  for i, member in enumerate(members):
    if ((member.bot == True) or (member.id == 441531704914739200)):
      indexes.append(i)
  for index in reversed(indexes):
    members.pop(index)
  # get number of players
  await ctx.send(f'係咪開{len(members)}人局？ (y/n)')
  msg = await bot.wait_for('message')
  if (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off')):
    await ctx.send('唔夠玩家！')
    pass
  else:
    # assign numbers to players
    await ctx.send('洗唔洗隨機分配號？ (y/n)')
    msg = await bot.wait_for('message')
    if (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off')):
      await ctx.send('請各位玩家依序回應')
      for i in range(1, len(members)+1):
        await ctx.send(f'{i}號玩家')
        msg = await bot.wait_for('message')
        index = members.index(msg.author)
        await members[index].edit(nick=i)
    else:
      print(f'{members}')
      random.shuffle(members)
      print(f'{members}')
      for i in range(1, len(members)+1):
        await members[i-1].edit(nick=i)

@bot.command(name='exit')
async def _exit(ctx: commands.Context):
  ctx.send('中止遊戲！')

bot.run(TOKEN)