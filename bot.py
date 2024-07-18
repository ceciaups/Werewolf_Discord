import os

import random
import re
import asyncio

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

class Player():
  def __init__(self, member, role, alive=True):
    self.member = member
    self.role = role
    self.alive = alive

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
  wgc = [4,4,4]
  set_wolf = [1,0,0,0]
  wolves = ['小狼', '白狼王', '黑狼王', '狼美人', '機械狼', '石像鬼', '夢魘', '血月使徒', '惡靈騎士', '隱狼/雪狼', '狼兄', '狼弟']
  set_good = [1,2,3,7,0,0,0,0]
  goods = ['平民', '預言家', '女巫', '獵人', '白痴', '騎士', '通靈師', '守衛', '守墓人', '攝夢人', '獵魔人', '魔術師', '黑市商人']
  set_all = []
  police = False
  speaktime = 0
  day = 0
  for i, member in enumerate(members):
    if ((member.bot == True) or (member.id == ADMIN_ID)):
      indexes.append(i)
  for index in reversed(indexes):
    members.pop(index)
  
  # test function
 
  pass

@bot.command(name='start')
async def _start(ctx: commands.Context):
  # await ctx.send('** \'!exit\'可以隨時離開遊戲！ **')

  # ------------------------------- General Variables -------------------------------
  wgc = [0, 0, 0]
  set_wolf = []
  wolves = ['小狼', '白狼王', '黑狼王', '狼美人', '機械狼', '石像鬼', '夢魘', '血月使徒', '惡靈騎士', '隱狼/雪狼', '狼兄', '狼弟']
  set_good = []
  goods = ['平民', '預言家', '女巫', '獵人', '白痴', '騎士', '通靈師', '守衛', '守墓人', '攝夢人', '獵魔人', '魔術師', '黑市商人']
  police = False
  speaktime = 0
  day = 0

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
  ans = await getYorN(ctx, f'係咪開{len(members)}人局？（y/n）')
  if (ans):
    # assign numbers to players
    ans = await getYorN(ctx, '洗唔洗隨機分配號？（y/n）')
    if (ans):
      random.shuffle(members)
      for i in range(1, len(members)+1):
        await members[i-1].edit(nick=i)
    else:
      await ctx.send('請各位玩家依序回應')
      for i in range(1, len(members)+1):
        index = await getMember(ctx, f'{i}號玩家')
        index = members.index(index[0])
        await members[index].edit(nick=i)
  else:
    await ctx.send('唔夠玩家！')
    return
  
  # --------------------------- CONFIGURE THE GAME: ROLES ---------------------------
  # wolves settings
  msg = None
  while (msg == None) or (not ans):
    # get number of wolves
    wgc[0] = await getNumber(ctx, f'幾狼？（1-{int(len(members)/2)}）', 1, 1, int(len(members)/2+1))
    # get type of wolves
    check_msg = ""
    set_wolf = []
    while (len(set_wolf) < wgc[0]):
      msg = await getNumber(ctx, f'請選擇狼嘅配置（輸入對應數字 0-{len(wolves)-2}）：\n╔═══╦═══════════════════╗\n║    0   ║                 其他全部小狼                 ║\n╠═══╬═══════╦═══╦═══════╣\n║    1    ║    白狼王     ║    6   ║       夢魘       ║\n╠═══╬═══════╬═══╬═══════╣\n║    2   ║    黑狼王     ║    7    ║  血月使徒  ║\n╠═══╬═══════╬═══╬═══════╣\n║    3   ║    狼美人     ║    8   ║   惡靈騎士  ║\n╠═══╬═══════╬═══╬═══════╣\n║    4   ║    機械狼     ║    9   ║  隱狼/雪狼 ║\n╠═══╬═══════╬═══╬═══════╣\n║    5   ║    石像鬼     ║   10  ║     狼兄弟    ║\n╚═══╩═══════╩═══╩═══════╝', 1, 0, len(wolves)-1)
      if (wolves[msg] in set_wolf):
        await ctx.send(f'已經有{wolves[msg]}！')
      elif (msg == wolves.index('小狼')):
        check_msg += str(wgc[0] - len(set_wolf)) + wolves[msg]
        for i in range(wgc[0] - len(set_wolf)):
          set_wolf.append(msg)
        await ctx.send(f'加咗{wolves[0]}')
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
        check_msg += wolves[msg]
        await ctx.send(f'加咗{wolves[msg]}')
    ans = await getYorN(ctx, f'{check_msg}，確認？（y/n）')
  # gods settings
  msg = None
  while (not msg) or (not ans):
    # get number of gods and citizen
    wgc[1] = await getNumber(ctx, f'幾神？（1-{len(members)-wgc[0]}）', 1, 1, len(members)-wgc[0]+1)
    wgc[2] = len(members) - sum(wgc)
    # get type of gods
    check_msg = ""
    set_good = []
    while (len(set_good) < wgc[1]):
      msg = await getNumber(ctx, f'請選擇神嘅配置（輸入對應數字 1-{len(goods)-1}）：\n╔═══╦═══════╦═══╦═══════╗\n║    1    ║    預言家     ║    7    ║       守衛      ║\n╠═══╬═══════╬═══╬═══════╣\n║    2   ║       女巫       ║   8    ║     守墓人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    3   ║       獵人       ║   9    ║     攝夢人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    4   ║       白痴       ║  10   ║     獵魔人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    5   ║       騎士       ║   11   ║     魔術師    ║\n╠═══╬═══════╬═══╬═══════╣\n║    6   ║     通靈師    ║   12   ║  黑市商人  ║\n╚═══╩═══════╩═══╩═══════╝', 1, 1, len(goods))
      if (goods[msg] in set_good):
        await ctx.send(f'已經有{goods[msg]}！')
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
    ans = await getYorN(ctx, f'{check_msg}，確認？（y/n）')

  # -------------------------- CONFIGURE THE GAME: SETTINGS --------------------------
  police = await getYorN(ctx, '上唔上警？（y/n）')
  speaktime = await getTimeInSeconds(ctx, '請輸入發言時間（mm:ss）')

  # ---------------------------------- STARTING THE GAME ----------------------------
  players = []
  for member in members:
    player = Player(member, '')
    players.append(player)
  await getMessage(ctx, '準備好請派牌！（輸入任何字元繼續遊戲)')
  await getMessage(ctx, '倒數三聲後可以確認身份，三，二，一', False, True, 15, False)
  while (0 not in wgc):
    await getMessage(ctx, '天黑請閉眼', False, True, 5, False)
    day += 1
    # night phase
    if (day == 1):
      msg1 = '請確認身份'
    else:
      msg1 = ''
    # 守衛
    if (7 in set_good):
      msg = None
      shield = 0
      while (not msg) or (not msg[0]):
        if (day == 1):
          timeout = 15
        else:
          timeout = 30
        await getMessage(ctx, '守衛請開眼，請選擇守護嘅對象', False, True, 0, False)
        shield = await getNumber(ctx, '', 1, 0, len(members)+1, True, True, 0, timeout)
        if (shield):
          index = await findPlayerByNumber(players, shield)
          if (players[index].alive):
            msg = await getYorN(ctx, f'{shield}號，確認？（y/n）', True, False, 0, 0, True)
          else:
            await getMessage(ctx, '請輸入存活嘅玩家', True, False, 5, False)
            msg = None
        elif (shield == 0):
          index = 0
          msg = await getYorN(ctx, f'空守，確認？（y/n）', True, False, 0, 0, True)
        else:
          msg = None
      if (day == 1):
        index = await findPlayerByNumber(players, int(msg[1]))
        players[index].role = goods[7]
    await getMessage(ctx, f'守衛請閉眼', False, True, 5, False)
    # 狼人
    msg = None
    while (day == 1) and (not msg):
      await getMessage(ctx, f'狼人請開眼，{msg1}', False, True, 0, False)
      for i, wolf in enumerate(set_wolf):
        if (wolf not in [0, 4, 5, 10, 11]):
          msg = await setRole(ctx, wolves[wolf], players)
          if (msg):
            players = msg
          else:
            break
        else:
          index = i
          break
      if (set_wolf[0] not in [0, 4, 5, 10, 11]) and (not msg):
        continue
      msg = await setRole(ctx, wolves[0], players, len(set_wolf)-index)
      if (msg):
        players = msg
    msg = None
    while (not msg):
      if (day == 1):
        msg = await getNumber(ctx, '狼人請殺人', 1, 0, len(members)+1, True, True)
      else:
        msg = await getNumber(ctx, '狼人請開眼，狼人請殺人', 1, 0, len(members)+1, True, True)
      if (msg):
        index = await findPlayerByNumber(players, msg)
        if (players[index].alive):
          msg = await getYorN(ctx, f'{msg}號，確認？（y/n）', True)
          if (msg):
            players[index].alive = False
            if (players[index].role in goods):
              if (players[index].role != goods[0]):
                wgc[1] -= 1
              else:
                wgc[2] -= 1
            elif (players[index].role in wolves):
              wgc[0] -= 1
        else:
          await getMessage(ctx, '請輸入存活嘅玩家', True, False, 5, False)
          msg = None
      elif (msg == 0):
        msg = await getYorN(ctx, f'空刀，確認？（y/n）', True)

  #   channel = client.get_channel(CHANNEL)
  #   command = message.content.strip()[len(BOT_PREFIX):].lower().split(' ')[0]
  #   parameters = message.content.strip().lower().split(' ')[1:]

@bot.command(name='exit')
async def _exit(ctx: commands.Context):
  ctx.send('中止遊戲！')

async def getYorN(ctx, q, delete=False, tts=False, delay=0, timeout=0, member=False):
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    if (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off', '唔係', '不', '不是', '否')):
      if (member):
        ans = [False, msg.author.nick]
      else:
        ans = False
    elif (msg.content.lower() in ('yes', 'y', 'true', 't', '1', 'enable', 'on', '係', '是')):
      if (member):
        ans = [True, msg.author.nick]
      else:
        ans = True
    else:
      if (delete) and (msg):
        await msg.delete()
      bmsg = await ctx.send('請回答y/n！')
      ans = await getYorN(ctx, q, delete, tts, delay, timeout, member)
      if (delete) and (bmsg):
        await bmsg.delete()
      return ans
    if (delete) and (msg):
      await msg.delete()
    return ans
  else:
    return msg

async def getNumber(ctx, q, x=1, min=0, max=100, delete=False, tts=False, delay=0, timeout=0):
  valid = True
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    ans = re.findall(r'\d+', msg.content)
    ans = list(map(int, ans))
    if (len(ans) == x):
      for index in ans:
        if (index not in range(min, max)):
          valid = False
      if (x == 1):
        ans = ans[0]
    else:
      valid = False
    if (valid):
      if (delete) and (msg):
        await msg.delete()
      return ans
    else:
      if (delete) and (msg):
        await msg.delete()
      bmsg = await ctx.send(f'請輸入啱嘅數字！（{min}-{max-1}）')
      ans = await getNumber(ctx, q, x, min, max, delete, tts, delay, timeout)
      if (delete) and (msg):
        await bmsg.delete()
      return ans
  else:
    return msg

async def getTimeInSeconds(ctx, q, delete=False, tts=False, delay=0, timeout=0):
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    if (re.match(r'\d{1,2}:\d{2}', msg.content)):
      msg = list(map(int, msg.content.split(':')))
      time = msg[0] * 60 + msg[1]
      return time
    else:
      await ctx.send('請輸入正確格式！（mm:ss）')
      return await getTimeInSeconds(ctx, q)
  else:
    return msg

async def getMember(ctx, q, delete=False, number=1, tts=False, delay=0, timeout=0, ans=[]):
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    if (msg.author in ans):
      if (delete) and (msg):
        await msg.delete()
      return await getMember(ctx, '', delete, number, tts, delay, timeout, ans)
    ans.append(msg.author)
    if (delete) and (msg):
      await msg.delete()
    if (number == 1):
      await getMessage(ctx, '收到！', False, False, 0, False)
    else:
      await getMessage(ctx, f'收到！-{number-1}', False, False, 0, False)
      ans = await getMember(ctx, '', delete, number-1, tts, delay, timeout, ans)
    return ans
  else:
    return msg

async def findPlayerByNumber(players, number):
  for x, player in enumerate(players):
    if (int(player.member.nick) == number):
      return x
  return None


async def setRole(ctx, role, players, x=1):
  authors = await getMember(ctx, f'{role}請輸入任何字元確認身份', True, x, False, 0, 15)
  if (authors):
    for author in authors:
      for player in players:
        if (player.member == author):
          player.role = role
  return players

async def getMessage(ctx, q, delete=False, tts=False, delay=0, get=True, timeout=0):
  if (q):
    bmsg = await ctx.send(q, tts=tts)
    await asyncio.sleep(delay)
  if (get):
    if (timeout):
      try:
        msg = await bot.wait_for('message', timeout=timeout)
      except asyncio.TimeoutError:
        if (delete and q):
          await bmsg.delete()
        return None
    else: 
      msg = await bot.wait_for('message')
    if (msg.author.bot == True):
      msg = await getMessage(ctx, '', delete, tts, delay, get, timeout)
  if (delete):
    if (q):
      await bmsg.delete()
  if (get):
    return msg
  else:
    return None

bot.run(TOKEN)