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
ADMIN_ID = int(os.getenv('DISCORD_ADMIN_ID'))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Class
# class Settings:
#   def __init__(self, config, number, players):
#     self.config = config
#     self.number = number
#     self.players = players

class Player(discord.Member):
  def __init__(self, role):
    self.role = role

# global settings variables
# roles = ""
# settings = Settings([], 0, [])

@bot.event
async def on_ready():
  # for guild in client.guilds:
  #       if guild.name == GUILD:
  #           break
  print(
    f'{bot.user} has connected to Discord!\n'
  )

@bot.command(name='test')
async def _test(ctx: commands.Context):
  members = ctx.channel.members
  indexes = []
  wgc = [4, 4, 4]
  set_wolf = []
  wolves = ['小狼', '白狼王', '黑狼王', '狼美人', '機械狼', '石像鬼', '夢魘', '血月使徒', '惡靈騎士', '隱狼/雪狼', '狼兄', '狼弟']
  set_good = []
  goods = ['平民', '預言家', '女巫', '獵人', '白痴', '騎士', '通靈師', '守衛', '守墓人', '攝夢人', '獵魔人', '魔術師', '黑市商人']
  for i, member in enumerate(members):
    if ((member.bot == True) or (member.id == ADMIN_ID)):
      indexes.append(i)
  for index in reversed(indexes):
    members.pop(index)
  
  # test function
  

  pass

@bot.command(name='start')
async def _start(ctx: commands.Context):
  await ctx.send('** \'!exit\'可以隨時離開遊戲！ **')

  # ------------------------------- General Variables -------------------------------
  wgc = []
  set_wolf = []
  wolves = ['小狼', '白狼王', '黑狼王', '狼美人', '機械狼', '石像鬼', '夢魘', '血月使徒', '惡靈騎士', '隱狼/雪狼', '狼兄', '狼弟']
  set_good = []
  goods = ['平民', '預言家', '女巫', '獵人', '白痴', '騎士', '通靈師', '守衛', '守墓人', '攝夢人', '獵魔人', '魔術師', '黑市商人']

  # -------------------------- CONFIGURE THE GAME: PLAYERS --------------------------
  members = ctx.channel.members
  # remove bot and admin
  indexes = []
  for i, member in enumerate(members):
    if ((member.bot == True) or (member.id == ADMIN_ID)):
      indexes.append(i)
  for index in reversed(indexes):
    members.pop(index)
  # get number of players
  await ctx.send(f'係咪開{len(members)}人局？（y/n）')
  msg = await bot.wait_for('message')
  if (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off')):
    await ctx.send('唔夠玩家！')
    return
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
      random.shuffle(members)
      for i in range(1, len(members)+1):
        await members[i-1].edit(nick=i)
  
  # -------------------------- CONFIGURE THE GAME: SETTINGS --------------------------
  # get number of wolves, gods, citizens
  while (sum(wgc) != len(members)) or (len(wgc) != 3):
    if (wgc):
      await ctx.send('唔啱數喎！')
    await ctx.send('幾狼幾神幾民？（3個數字）')
    msg = await bot.wait_for('message')
    wgc = list(map(int, re.findall(r'\d+', msg.content)))
  # get type of wolves
  msg = None
  while (not msg) or (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off')):
    check_msg = ""
    set_wolf = []
    await ctx.send('請選擇狼嘅配置（輸入對應數字 0-10）：\n╔═══╦═══════════════════╗\n║    0   ║                 其他全部小狼                 ║\n╠═══╬═══════╦═══╦═══════╣\n║    1    ║    白狼王     ║    6   ║       夢魘       ║\n╠═══╬═══════╬═══╬═══════╣\n║    2   ║    黑狼王     ║    7    ║  血月使徒  ║\n╠═══╬═══════╬═══╬═══════╣\n║    3   ║    狼美人     ║    8   ║   惡靈騎士  ║\n╠═══╬═══════╬═══╬═══════╣\n║    4   ║    機械狼     ║    9   ║  隱狼/雪狼 ║\n╠═══╬═══════╬═══╬═══════╣\n║    5   ║    石像鬼     ║   10  ║     狼兄弟    ║\n╚═══╩═══════╩═══╩═══════╝')
    while (len(set_wolf) < wgc[0]):
      msg = await bot.wait_for('message')
      msg = int(re.search(r'\d+', msg.content).group())
      if (msg >= len(wolves)) or (msg < 0):
        await ctx.send(f'請輸入啱嘅數字！（0-{len(wolves)-1}）')
      elif (msg == wolves.index('小狼')):
        check_msg += str(wgc[0] - len(set_wolf)) + wolves[msg]
        for i in range(wgc[0] - len(set_wolf)):
          set_wolf.append(msg)
      elif (msg == wolves.index('狼兄')):
        if (wgc[0] - len(set_wolf) > 1):
          set_wolf.append(msg)
          set_wolf.append(msg+1)
          check_msg += '1' + wolves[msg] + '1' + wolves[msg+1]
          await ctx.send(f'加咗{wolves[msg]}{wolves[msg+1]}')
        else:
          await ctx.send(f'唔夠兩隻狼，加唔到！')
      else:
        set_wolf.append(msg)
        check_msg += '1' + wolves[msg]
        await ctx.send(f'加咗{wolves[msg]}')
    await ctx.send(f'{check_msg}，確認？（y/n）')
    msg = await bot.wait_for('message')
  # get type of gods
  msg = None
  while (not msg) or (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off')):
    check_msg = ""
    set_good = []
    await ctx.send('請選擇神嘅配置（輸入對應數字 1-13）：\n╔═══╦═══════╦═══╦═══════╗\n║    1    ║    預言家     ║    7    ║       守衛      ║\n╠═══╬═══════╬═══╬═══════╣\n║    2   ║       女巫       ║   8    ║     守墓人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    3   ║       獵人       ║   9    ║     攝夢人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    4   ║       白痴       ║  10   ║     獵魔人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    5   ║       騎士       ║   11   ║     魔術師    ║\n╠═══╬═══════╬═══╬═══════╣\n║    6   ║     通靈師    ║   12   ║  黑市商人  ║\n╚═══╩═══════╩═══╩═══════╝')
    while (len(set_good) < wgc[1]):
      msg = await bot.wait_for('message')
      msg = int(re.search(r'\d+', msg.content).group())
      if (msg >= len(goods)) or (msg < 1):
        await ctx.send(f'請輸入啱嘅數字！（1-{len(goods)-1}）')
      else:
        set_good.append(msg)
        await ctx.send(f'加咗{goods[msg]}')
        if (msg < 8):
          check_msg += goods[msg][0]
        else:
          check_msg += goods[msg]
    check_msg += str(wgc[2]) + goods[0]
    for i in range(wgc[2]):
      set_good.append(0)
    await ctx.send(f'{check_msg}，確認？（y/n）')
    msg = await bot.wait_for('message')

  #   channel = client.get_channel(CHANNEL)
  #   command = message.content.strip()[len(BOT_PREFIX):].lower().split(' ')[0]
  #   parameters = message.content.strip().lower().split(' ')[1:]

@bot.command(name='exit')
async def _exit(ctx: commands.Context):
  ctx.send('中止遊戲！')

bot.run(TOKEN)