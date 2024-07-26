import os

import random
import re
import asyncio
import math
from datetime import datetime

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

class Player():
  def __init__(self, member, role, alive=True):
    self.member = member
    self.role = role
    self.alive = alive

@bot.event
async def on_ready():
  print(
    f'{bot.user} has connected to Discord!\n'
  )

# test function
@bot.command(name='test')
async def _test(ctx: commands.Context):
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
  sheriff = False
  speaktime = 0

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
  # ans = await getYorN(ctx, f'係咪開{len(members)}人局？（y/n）')
  # if (ans):
  #   # assign numbers to players
  #   ans = await getYorN(ctx, '隨機分配號碼？（y/n）')
  #   if (ans):
  #     random.shuffle(members)
  #     for i in range(1, len(members)+1):
  #       await members[i-1].edit(nick=i)
  #   else:
  #     await ctx.send('請各位玩家依序回應')
  #     for i in range(1, len(members)+1):
  #       index = await getMember(ctx, f'{i}號玩家')
  #       index = members.index(index[0])
  #       await members[index].edit(nick=i)
  # else:
  #   await ctx.send('不夠玩家！')
  #   return
  
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
      msg = await getNumber(ctx, f'請選擇狼的配置（輸入對應數字 0-{len(wolves)-2}）：\n╔═══╦═══════════════════╗\n║    0   ║                 其他全部小狼                 ║\n╠═══╬═══════╦═══╦═══════╣\n║    1    ║    白狼王     ║    6   ║       夢魘       ║\n╠═══╬═══════╬═══╬═══════╣\n║    2   ║    黑狼王     ║    7    ║  血月使徒  ║\n╠═══╬═══════╬═══╬═══════╣\n║    3   ║    狼美人     ║    8   ║   惡靈騎士  ║\n╠═══╬═══════╬═══╬═══════╣\n║    4   ║    機械狼     ║    9   ║  隱狼/雪狼 ║\n╠═══╬═══════╬═══╬═══════╣\n║    5   ║    石像鬼     ║   10  ║     狼兄弟    ║\n╚═══╩═══════╩═══╩═══════╝', 1, 0, len(wolves)-1)
      if (wolves[msg] in set_wolf):
        await ctx.send(f'已經有{wolves[msg]}！')
      elif (msg == wolves.index('小狼')):
        check_msg += str(wgc[0] - len(set_wolf)) + wolves[msg]
        for i in range(wgc[0] - len(set_wolf)):
          set_wolf.append(msg)
        await ctx.send(f'加了{wolves[0]}')
      elif (msg == wolves.index('狼兄')):
        if (wgc[0] - len(set_wolf) > 1):
          set_wolf.append(msg)
          set_wolf.append(msg+1)
          check_msg += '1' + wolves[msg] + '1' + wolves[msg+1]
          await ctx.send(f'加了{wolves[msg]}{wolves[msg+1]}')
        else:
          await ctx.send(f'不夠兩隻狼，加不到！')
      else:
        set_wolf.append(msg)
        check_msg += wolves[msg]
        await ctx.send(f'加了{wolves[msg]}')
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
      msg = await getNumber(ctx, f'請選擇神的配置（輸入對應數字 1-{len(goods)-1}）：\n╔═══╦═══════╦═══╦═══════╗\n║    1    ║    預言家     ║    7    ║       守衛      ║\n╠═══╬═══════╬═══╬═══════╣\n║    2   ║       女巫       ║   8    ║     守墓人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    3   ║       獵人       ║   9    ║     攝夢人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    4   ║       白痴       ║  10   ║     獵魔人    ║\n╠═══╬═══════╬═══╬═══════╣\n║    5   ║       騎士       ║   11   ║     魔術師    ║\n╠═══╬═══════╬═══╬═══════╣\n║    6   ║     通靈師    ║   12   ║  黑市商人  ║\n╚═══╩═══════╩═══╩═══════╝', 1, 1, len(goods))
      if (goods[msg] in set_good):
        await ctx.send(f'已經有{goods[msg]}！')
      else:
        set_good.append(msg)
        await ctx.send(f'加了{goods[msg]}')
        if (msg < 8):
          check_msg += goods[msg][0]
        else:
          check_msg += goods[msg]
    check_msg += str(wgc[2]) + goods[0]
    for i in range(wgc[2]):
      set_good.append(0)
    ans = await getYorN(ctx, f'{check_msg}，確認？（y/n）')

  # -------------------------- CONFIGURE THE GAME: SETTINGS --------------------------
  # sheriff = await getYorN(ctx, '上不上警？（y/n）')
  # speaktime = await getTimeInSeconds(ctx, '請輸入發言時間（mm:ss）')

  # ---------------------------------- STARTING THE GAME ----------------------------
  players = []
  for member in members:
    player = Player(member, '')
    players.append(player)
  if (wgc[0] > 3):
    no_sheriff = [2, False]
  else:
    no_sheriff = [1, False]
  await getMessage(ctx, '準備好請派牌！（輸入任何字元繼續遊戲)')
  await getMessage(ctx, '倒數三聲後可以確認身份，三，二，一', False, True, 15, False)
  day = 0
  shield = 0
  sleep = [0,False,0]
  magic_history = []
  witcher = [0, 0]
  add = []
  knight = False
  lucky = [0,0,0]
  special = 0
  special_day = 0
  while (0 not in wgc):
    day += 1
    if (12 in set_good):
      print('----------before----------')
      random.shuffle(players)
      special = random.randint(1,len(players)+1)
      for i, player in enumerate(players):
        print(f'{player.member}, {player.member.nick}, {player.role}, {player.alive}')
        if (i+1 == special):
          await getMessage(player.member, f'你的幸運號碼是{len(players)+1}！', False, False, 0, False)
        else:
          await getMessage(player.member, f'你的幸運號碼是{i+1}！', False, False, 0, False)
      await getMessage(ctx, '請確認自己的幸運號碼（輸入任何字元繼續遊戲)')
    await getMessage(ctx, '天黑請閉眼', False, True, 5, False)
    wolf_kill = 1
    kills = [0]
    super_kill = []
    magic = []
    sleep[1] = False
    broken = False
    no_sheriff[1] = False
    night = False
    guns = []

    # night phase
    if (day == 1):
      timeout = 15
      msg1 = '請確認身份'
    else:
      timeout = 30
      msg1 = ''
    # 守衛
    role_number = 7
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      msg = None
      index = await findPlayerByRole(players, goods[role_number])
      while (not msg):
        if (day == 1):
          await getMessage(ctx, f'請選擇守護的對象', False, True, 0, False)
        else:
          await getMessage(ctx, f'{goods[role_number]}請睜眼，請選擇守護的對象', False, True, 0, False)
        if (players[index].alive):
          msg = await getNumber(ctx, '', 1, 0, len(members)+1, True, False, 0, timeout)
          if (msg != None):
            if (msg) and (msg != shield):
              temp = msg
              temp_i = await findPlayerByNumber(players, temp)
              if (players[temp_i].alive):
                msg = await getYorN(ctx, f'守{temp}號，確認？（y/n）', True, False, 0, 0)
                if (msg):
                  shield = temp
              else:
                await getMessage(ctx, '請輸入存活的玩家！', True, False, 5, False)
                msg = None
            elif (msg) and (msg == shield):
              await getMessage(ctx, '不可以連續兩日守護同一位玩家！', True, False, 5, False)
              msg = None
            elif (msg == 0):
              msg = await getYorN(ctx, f'空守，確認？（y/n）', True, False, 0, 0)
              if (msg):
                shield = 0
        else:
          await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 8, False)
          msg = True
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 攝夢人
    role_number = 9
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
          index = await findPlayerByRole(players, goods[role_number])
          sleep[2] = int(players[index].member.nick)
      msg = None
      index = await findPlayerByRole(players, goods[role_number])
      while (not msg):
        if (day == 1):
          await getMessage(ctx, f'請選擇夢遊的對象', False, True, 0, False)
        else:
          await getMessage(ctx, f'{goods[role_number]}請睜眼，請選擇夢遊的對象', False, True, 0, False)
        if (players[index].alive):
          msg = await getNumber(ctx, '', 1, 1, len(members)+1, True, False, 0, timeout)
          if (msg != None):
            if (msg):
              temp = msg
              temp_i = await findPlayerByNumber(players, msg)
              if (players[temp_i].alive):
                if (msg != sleep[0]):
                  msg = await getYorN(ctx, f'夢{temp}號，確認？（y/n）', True, False, 0, 0)
                  if (msg):
                    sleep[0] = temp
                else:
                  msg = await getYorN(ctx, f'連續兩日夢{temp}號，確認？（y/n）', True, False, 0, 0)
                  if (msg):
                    sleep[1] = True
                    kills.append(temp)
              else:
                await getMessage(ctx, '請輸入存活的玩家！', True, False, 5, False)
                msg = None
        else:
          await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 8, False)
          msg = True
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 魔術師
    role_number = 11
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      msg = None
      index = await findPlayerByRole(players, goods[role_number])
      while (not msg):
        magic = []
        if (day == 1):
          await getMessage(ctx, f'請選擇交換的對象', False, True, 0, False)
        else:
          await getMessage(ctx, f'{goods[role_number]}請睜眼，請選擇交換的對象', False, True, 0, False)
        if (players[index].alive):
          if (len(players) - len(magic_history) >= 2):
            msg = await getNumber(ctx, '', 2, 0, len(members)+1, True, False, 0, timeout)
            if (msg != None):
              if (len(msg) == 1):
                msg = await getYorN(ctx, f'空換，確認？（y/n）', True, False, 0, 0)
              elif (msg[0] not in magic_history) and (msg[1] not in magic_history):
                magic = msg
                msg = await getYorN(ctx, f'換{magic[0]}號同{magic[1]}號，確認？（y/n）', True, False, 0, 0)
              else:
                await getMessage(ctx, f'不可以換已經出局/交換過的玩家！{magic_history}', True, False, 5, False)
                msg = None
          else:
            await getMessage(ctx, f'無足夠的玩家交換，自動空守！{magic_history}', True, False, 5, False)
            magic = []
            msg = True
        else:
          await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 8, False)
          msg = True
      magic_history.extend(magic)
      magic_history.sort()
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 狼兄狼弟
    role_number = 10
    if (role_number in set_wolf):
      if (day == 1):
        msg = None
        while (not msg):
          await getMessage(ctx, f'{wolves[role_number]}{wolves[role_number+1]}請睜眼，{msg1}', False, True, 0, False)
          msg = await setRole(ctx, wolves[role_number], players)
          if (msg):
            players = msg
            msg = await setRole(ctx, wolves[role_number+1], players)
            if (msg):
              players = msg
        await getMessage(ctx, f'{wolves[role_number]}{wolves[role_number+1]}請閉眼', False, True, 5, False)
      else:
        msg = None
        index1 = await findPlayerByRole(players, wolves[role_number])
        index2 = await findPlayerByRole(players, wolves[role_number+1])
        while (not msg):
          await getMessage(ctx, f'{wolves[role_number+1]}請睜眼，請選擇你要復仇的對象。', False, True, 0, False)
          if (players[index2].alive):
            if (players[index1].alive):
              await getMessage(ctx, f'{wolves[role_number]}仲未出局，未有復仇刀！', True, False, 10, False)
              msg = True
            else:
              msg = await getNumber(ctx, '', 1, 1, len(members)+1, True, False, 0, timeout)
              if (msg):
                temp = msg
                temp_i = await findPlayerByNumber(players, temp)
                if (players[temp_i].alive):
                  msg = await getYorN(ctx, f'刀{temp}號，確認？（y/n）', True)
                  if (msg):
                    kills.insert(1,temp)
                    wolf_kill += 1
                else:
                  await getMessage(ctx, '請輸入存活的玩家！', True, False, 5, False)
                  msg = None
          else:
            await getMessage(ctx, f'{wolves[role_number+1]}已出局！', True, False, 10, False)
            msg = True
        await getMessage(ctx, f'{wolves[role_number+1]}請閉眼', False, True, 5, False)
    # 狼人
    msg = None
    while (day == 1) and (not msg):
      await getMessage(ctx, f'狼人請睜眼，{msg1}', False, True, 0, False)
      for i, wolf in enumerate(set_wolf):
        if (wolf not in [0, 4, 5, 10, 11]):
          msg = await setRole(ctx, wolves[wolf], players)
          if (msg):
            players = msg
        else:
          msg = True
          index = i
          if (wolf == 0):
            break
      if (msg) and (0 in set_wolf):
          msg = await setRole(ctx, wolves[0], players, len(set_wolf)-index)
          if (msg):
            players = msg
    msg = None
    while (not msg):
      kills[0] = 0
      if (day == 1):
        msg = await getNumber(ctx, '狼人請殺人', 1, 0, len(members)+1, True, True)
      else:
        msg = await getNumber(ctx, '狼人請睜眼，狼人請殺人', 1, 0, len(members)+1, True, True)
      if (msg):
        kills[0] = msg
        index = await findPlayerByNumber(players, kills[0])
        if (players[index].alive):
          msg = await getYorN(ctx, f'刀{kills[0]}號，確認？（y/n）', True)
        else:
          await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
          msg = None
      elif (msg == 0):
        msg = await getYorN(ctx, '空刀，確認？（y/n）', True)
    await getMessage(ctx, '狼人請閉眼', False, True, 5, False)
    # 獵魔人
    role_number = 10
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      index = await findPlayerByRole(players, goods[role_number])
      while (day != 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，請選擇你要獵殺的對象', False, True, 0, False)
        if (players[index].alive):
          msg = await getNumber(ctx, '', 1, 0, len(members)+1, True, False, 0, timeout)
          if (msg):
            temp = msg
            temp_i = await findPlayerByNumber(players, msg)
            if (players[temp_i].alive):
              msg = await getYorN(ctx, f'獵{temp}號，確認？（y/n）', True, False, 0, 0)
              if (msg) and (players[temp_i].role in wolves):
                kills.append(int(players[temp_i].member.nick))
              else:
                kills.append(int(players[index].member.nick))
            else:
              await getMessage(ctx, '請輸入存活的玩家！', True, False, 5, False)
              msg = None
          elif (msg == 0):
            msg = await getYorN(ctx, f'不獵殺，確認？（y/n）', True)
        else:
          await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 8, False)
          msg = True
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 女巫
    role_number = 2
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      msg = None
      index = await findPlayerByRole(players, goods[role_number])
      while (not msg):
        msg = False
        if (day == 1):
          await getMessage(ctx, '請問你要不要用救藥？', False, True, 0, False)
        else:
          await getMessage(ctx, f'{goods[role_number]}請睜眼，請問你要不要用救藥？', False, True, 0, False)
        if (not witcher[0]) and (kills[0] != int(players[index].member.nick)) and (players[index].alive):
          msg = await getYorN(ctx, f'{kills[0]}號死了，要不要救？（y/n）', True, False, 0, timeout)
        if (msg):
          msg = await getYorN(ctx, f'救{kills[0]}號，確認？（y/n）', True)
          if (msg):
            witcher[0] = kills[0]
            if (kills[0] != shield):
              kills.pop(0)
              wolf_kill -= 1
            else:
              broken = True
            await getMessage(ctx, '請問你要不要用毒藥？', False, True, 0, False)
            await getMessage(ctx, '你用了救藥，不能在同一晚用毒藥！', True, False, 5, False)
        elif (msg != None):
          if (players[index].alive):
            if (not witcher[0]) and (kills[0] == int(players[index].member.nick)):
              await getMessage(ctx, '你中狼刀，不能自救！', True, False, 8, False)
            elif (not witcher[0]):
              await getMessage(ctx, '不用救藥！', True, False, 8, False)
            else:
              await getMessage(ctx, '救藥已經用完！', True, False, 8, False)
          else:
             await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 8, False)
          await getMessage(ctx, '請問你要不要用毒藥？', False, True, 0, False)
          if (not witcher[1]) and (players[index].alive):
            msg = await getNumber(ctx, f'不毒請輸入0，毒請輸入1-{len(members)}', 1, 0, len(members)+1, True, False, 0, timeout)
            if (msg):
              index = await findPlayerByNumber(players, msg)
              if (players[index].alive):
                msg = await getYorN(ctx, f'毒{msg}號，確認？（y/n）', True)
                if (msg):
                  witcher[1] = int(players[index].member.nick)
                  if (players[index].role != goods[10]):
                    kills.append(int(players[index].member.nick))
              else:
                await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
                msg = None
            elif (msg != None):
              msg = await getYorN(ctx, f'不用毒藥，確認？（y/n）', True)
          elif (players[index].alive):
            await getMessage(ctx, '毒藥已經用完！', True, False, 10, False)
            msg = True
          else:
            await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 10, False)
            msg = True
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 黑市商人
    role_number = 12
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      msg = None
      index = await findPlayerByRole(players, goods[role_number])
      while (not msg):
        if (day == 1):
          await getMessage(ctx, f'請選擇你要交易的對象是：', False, True, 0, False)
        else:
          await getMessage(ctx, f'{goods[role_number]}請睜眼，請選擇你要交易的對象是：', False, True, 0, False)
        if (players[index].alive):
          if (lucky[0]):
            await getMessage(ctx, '交易已經完成！', True, False, 8, False)
            msg = True
          else:
            msg = await getNumber(ctx, '', 1, 0, len(members)+1, True, False, 0, timeout)
            if (msg == 0):
              msg = await getYorN(ctx, f'不交易，確認？（y/n）', True)
            elif (msg == int(players[index].member.nick)):
              await getMessage(ctx, '不可以與自己交易！', True, False, 3, False)
              msg = None
            elif (msg):
              temp = msg
              temp_i = await findPlayerByNumber(players, msg)
              if (players[temp_i].alive):
                temp1 = await getNumber(ctx, '你要交易的技能是：（1：水晶球，2：毒藥，3：獵槍）', 1, 1, 4, True, False)
                if (temp1 == 1):
                  temp_s = '水晶球'
                elif (temp1 == 2):
                  temp_s = '毒藥'
                elif (temp1 == 3):
                  temp_s = '獵槍'
                msg = await getYorN(ctx, f'與{temp}號交易{temp_s}，確認？（y/n）', True, False, 0, 0)
                if (msg) and (players[temp_i].role in wolves):
                  kills.append(int(players[index].member.nick))
                elif (msg):
                  lucky = [temp, temp1, 0]
                  special_day = day
              else:
                await getMessage(ctx, '請輸入存活的玩家！', True, False, 3, False)
                msg = None
        else:
          await getMessage(ctx, f'{goods[role_number]}已出局！', True, False, 8, False)
          msg = True
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
      for player in players:
        if (int(player.member.nick) == lucky[0]):
          skill = ''
          if (lucky[1] == 1):
            skill = '水晶球'
          elif (lucky[1] == 2):
            skill = '毒藥'
          elif (lucky[1] == 3):
            skill = '獵槍，你今晚的開槍狀態是'
            index = lucky[0]
            if (int(players[index].member.nick) in magic):
              if (magic[0] == int(players[index].member.nick)):
                index = magic[1]
              else:
                index = magic[0]
            else:
              index = int(players[index].member.nick)
            if (index == witcher[1]) or ((index == sleep[0]) and (sleep[1])) or ((index == sleep[0]) and (sleep[2] in kills)) or (index == lucky[2]):
              skill += 'No 👎'
            else:
              skill += 'Yes 👍'
          await getMessage(player.member, f'你是幸運兒，你獲得{skill}！', False, False, 0, False)
        else:
          await getMessage(player.member, '你不是幸運兒！', False, False, 0, False)
      msg = None
      while (not msg):
        if (not lucky[0]):
          await getMessage(ctx, f'幸運號碼{special}號請睜眼，請問你要用技能嗎？', False, True, 0, False)
          await getMessage(ctx, '沒有幸運兒！', True, False, 10, False)
          msg = True
        else:
          index = await findPlayerByNumber(players, lucky[0])
          if (index+1 == special):
            await getMessage(ctx, f'幸運號碼{len(players)+1}號請睜眼，請問你要用技能嗎？', False, True, 0, False)
          else:
            await getMessage(ctx, f'幸運號碼{index+1}號請睜眼，請問你要用技能嗎？', False, True, 0, False)
          if (players[index].alive):
            if (lucky[1] == 1):
              if (special_day < day):
                msg = True
                msg = await getNumber(ctx, f'請輸入1-{len(members)}查驗一個人的身份', 1, 1, len(members)+1, True, False, 0, timeout)
                if (msg):
                  index = await findPlayerByNumber(players, msg)
                  if (not players[index].alive):
                    await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
                    msg = None
                  elif (players[index].role in wolves):
                    await getMessage(ctx, f'{msg}號的身份是狼人！', True, False, 8, False)
                  else:
                    await getMessage(ctx, f'{msg}號的身份是好人！', True, False, 8, False)
              else: 
                await getMessage(ctx, '你獲得水晶球，要第二日才能查驗身份！', True, False, 10, False)
                msg = True
            elif (lucky[1] == 2):
              if (special_day < day):
                msg = await getNumber(ctx, f'不毒請輸入0，毒請輸入1-{len(members)}', 1, 0, len(members)+1, True, False, 0, timeout)
                if (msg):
                  index = await findPlayerByNumber(players, msg)
                  if (not players[index].alive):
                    await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
                    msg = None
                  else:
                    lucky[2] = int(players[index].member.nick)
                    lucky[1] = 0
                    if (players[index].role != goods[10]):
                        kills.append(int(players[index].member.nick))
                elif (msg == 0):
                  msg = True
              else:
                await getMessage(ctx, '你獲得毒藥，要第二日才能開毒！', True, False, 10, False)
                msg = True
            elif (lucky[1] == 3):
              msg = await getMessage(ctx, '請輸入任何字元繼續遊戲', True, False, 0, True, timeout)
              if (msg):
                await msg.delete()
                if (int(players[index].member.nick) in magic):
                  if (magic[0] == int(players[index].member.nick)):
                    index = magic[1]
                  else:
                    index = magic[0]
                else:
                  index = int(players[index].member.nick)
                if (index == witcher[1]) or ((index == sleep[0]) and (sleep[1])) or ((index == sleep[0]) and (sleep[2] in kills)) or (index == lucky[2]):
                  await getMessage(ctx, '你今晚的開槍狀態是：No 👎', True, False, 5, False)
                else:
                  await getMessage(ctx, '你今晚的開槍狀態是：Yes 👍', True, False, 5, False)
                  guns.append(lucky[0])
                msg = True
            else:
              await getMessage(ctx, f'技能已經用完！', True, False, 10, False)
              msg = True
          else:
            await getMessage(ctx, '幸運兒已出局！', True, False, 10, False)
            msg = True
      await getMessage(ctx, '幸運兒請閉眼！', False, True, 5, False)
    # 獵人
    role_number = 3
    if (role_number in set_good):
      msg = None
      while (not msg):
        if (day == 1):
          await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
          msg = await setRole(ctx, goods[role_number], players)
          if (msg):
            players = msg
        else:
          await getMessage(ctx, f'{goods[role_number]}請睜眼', False, True, 0, False)
          msg = await getMessage(ctx, '請輸入任何字元繼續遊戲', True, False, 0, True, timeout)
          await msg.delete()
      index = await findPlayerByRole(players, goods[role_number])
      await getMessage(ctx, '你今晚的開槍狀態是：', False, True, 0, False)
      if (int(players[index].member.nick) in magic):
        if (magic[0] == int(players[index].member.nick)):
          temp_i = magic[1]
        else:
          temp_i = magic[0]
      else:
        temp_i = int(players[index].member.nick)
      if (temp_i == witcher[1]) or ((temp_i == sleep[0]) and (sleep[1])) or ((temp_i == sleep[0]) and (sleep[2] in kills)) or (temp_i == lucky[2]):
        await getMessage(ctx, 'No 👎', True, False, 5, False)
      else:
        await getMessage(ctx, 'Yes 👍', True, False, 5, False)
        guns.append(int(players[index].member.nick))
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 白痴
    role_number = 4
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 騎士
    role_number = 5
    if (role_number in set_good):
      msg = None
      while (day == 1) and (not msg):
        await getMessage(ctx, f'{goods[role_number]}請睜眼，{msg1}', False, True, 0, False)
        msg = await setRole(ctx, goods[role_number], players)
        if (msg):
          players = msg
      await getMessage(ctx, f'{goods[role_number]}請閉眼', False, True, 5, False)
    # 平民
    if (day == 1):
      for player in players:
        if (not player.role):
          player.role = goods[0]
    # 上警發言
    if (day == 1) and (sheriff):
      await getMessage(ctx, f'要上警的玩家請舉手！', False, True, 5, False)
      await getMessage(ctx, f'天亮請睜眼！', False, True, 0, False)
      temp_sheriff = await getNumber(ctx, '請問有幾多位玩家上警？', 1, 1, len(members)+1)
      if (temp_sheriff > 1):
        number = random.randint(1,len(members))
        direction = random.randint(1,2)
        msg = f'{number}號，'
        if (direction == 1):
          msg += '逆向開始發言'
        else:
          msg += '順向開始發言'
        await getMessage(ctx, f'{msg}', False, True, 0, False)
        await getMessage(ctx, '加時輸入\'+\'，自爆輸入\'0\'，使用技能輸入\'s\'，跳過發言輸入任何字元', False, False, 3, False)
        for i in range(temp_sheriff):
          add = await listenSpeech(ctx, False, speaktime, add)
          if (add[1] == 'skill'):
            index = await findPlayerByNumber(players, add[2])
            role = players[index].role
            if (goods[5] == role):
              if (not knight):
                msg = await getNumber(ctx, f'請輸入要撞的對象是：', 1, 0, len(members)+1, False, True, 0, 0)
                if (msg):
                  index1 = await findPlayerByNumber(players, msg)
                  role1 = players[index1].role
                  if (players[index1].alive) and (role1 in wolves):
                    await getMessage(ctx, f'{msg}號是狼人，{msg}號淘汰！', False, True, 3, False)
                    players[index1].alive = False
                    knight = True
                    no_sheriff[1] = True
                    break
                  elif (players[index1].alive):
                    await getMessage(ctx, f'{msg}號不是狼人，{players[index].member.nick}號以死謝罪！', False, True, 3, False)
                    players[index].alive = False
                    knight = True
                  else:
                    await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
                    msg = None
              else:
                await getMessage(ctx, '騎士技能已經用過！', False, False, 0, False)
            else:
              await getMessage(ctx, '沒有技能可以使用！', False, False, 0, False)
            add = add[0]
          elif (add[1] == 'explode'):
            index = await findPlayerByNumber(players, add[2])
            players[index].alive = False
            if (players[index].role in goods):
              if (players[index].role != goods[0]):
                wgc[1] -= 1
              else:
                wgc[2] -= 1
            elif (players[index].role in wolves):
              wgc[0] -= 1
            no_sheriff[0] -= 1
            no_sheriff[1] = True
            add = add[0]
            if (not no_sheriff[0]):
              sheriff = False
              await getMessage(ctx, f'今場將沒有警徽！', False, True, 3, False)
            break
          else:
            add = add[0]
          if (i + 1 != temp_sheriff):
            await getMessage(ctx, '下一位開始發言', True, False, 3, False)
      else:
        await getMessage(ctx, '直接當選警長！', False, True, 5, False)
    if (sheriff == True) and (no_sheriff[0]) and (not no_sheriff[1]):
      msg = None
      if (temp_sheriff > 1):
        msg = await getMessage(ctx, '仍然在警上的玩家請舉手！', False, True, 0, True, 5)
        if (not msg):
          msg = await getMessage(ctx, '請用投票功能/自行選出警長！', False, False, 0, True, 5)
      if (msg):
        msg = [msg.content.lower(), int(msg.author.nick)]
      else:
        msg = [msg, msg]
      if (not msg[0]):
        msg = await getNumber(ctx, f'請輸入當選警長的玩家是：', 1, 0, len(members)+1, True, False, 0, 0, True)
      if (msg[0] in (0, '0', 'e', 'explode', '爆', '自爆')):
        await getMessage(ctx, f'{msg[1]}號自爆！', False, True, 3, False)
        index = await findPlayerByNumber(players, msg[1])
        players[index].alive = False
        if (players[index].role in goods):
          if (players[index].role != goods[0]):
            wgc[1] -= 1
          else:
            wgc[2] -= 1
        elif (players[index].role in wolves):
          wgc[0] -= 1
        no_sheriff[0] -= 1
        no_sheriff[1] = True
        if (not no_sheriff[0]):
          sheriff = False
          await getMessage(ctx, f'今場將沒有警徽！', False, True, 3, False)
      else:
        sheriff = msg[0]
        await getMessage(ctx, f'{sheriff}號當選警長！', False, True, 5, False)
    # 夜刀
    count = 0
    if (wolf_kill > 1):
      for x in range(wolf_kill):
        temp_kill = kills[wolf_kill-x-1:wolf_kill]
        if (temp_kill.count(temp_kill[0]) > 1):
          super_kill.append(temp_kill[0])
          kills.pop(wolf_kill-x-1)
    super_kill = list(dict.fromkeys(super_kill))
    kills = list(dict.fromkeys(kills))
    for x, kill in enumerate(reversed(kills)):
      if (kill):
        valid = True
        if ((len(kills)-x) <= wolf_kill) and (kill not in super_kill):
          if (shield == kill) and (not broken):
            valid = False
        if (kill == sleep[0]) and (not sleep[1]) and (kill not in super_kill):
          valid = False
        if (kill == sleep[2]):
          kills.append(sleep[0])
          count += 1
          index = await findPlayerByNumber(players, sleep[0])
          if (players[index].role in goods):
            if (players[index].role != goods[0]):
              wgc[1] -= 1
            else:
              wgc[2] -= 1
          elif (players[index].role in wolves):
            wgc[0] -= 1
        if (valid):
          if (kill in magic):
            kills.pop(len(kills)-x-1)
            if (kill == magic[0]):
              kills.insert(len(kills)-x-1, magic[1])
              kill = magic[1]
            else:
              kills.insert(len(kills)-x-1, magic[0])
              kill = magic[0]
          index = await findPlayerByNumber(players, kill)
          if (int(players[index].member.nick) not in magic_history):
            magic_history.append(int(players[index].member.nick))
            magic_history.sort()
          if (players[index].role in goods):
            if (players[index].role != goods[0]):
              wgc[1] -= 1
            else:
              wgc[2] -= 1
          elif (players[index].role in wolves):
            wgc[0] -= 1
        else:
          kills.pop(len(kills)-x-1-count)
    kills.sort()
    # 天光公報死訴
    for kill in kills:
      index = await findPlayerByNumber(players, kill)
      players[index].alive = False 
    if (len(kills) == 0) and (not sheriff):
      await getMessage(ctx, f'天亮請睜眼，昨晚是平安夜！', False, True, 5, False)
    elif (len(kills) == 0):
      await getMessage(ctx, f'昨晚是平安夜！', False, True, 5, False)
    else:
      if (day != 1) or (not sheriff):
        msg = '天亮請睜眼，昨晚'
      else:
        msg = '昨晚'
      for x, i in enumerate(kills):
        msg += str(i)
        msg += '號'
        if (x != len(kills)-1):
          msg += '、'
      msg += '被殺死！'
      await getMessage(ctx, f'{msg}', False, True, 5, False)
    # 夜槍
    msg = None
    if (len(guns)):
      temp_kill = []
      for gun in guns:
        if (int(gun) in kills):
          msg = None
          while (not msg):
            msg = await getNumber(ctx, f'{gun}號發動角色技能，你要帶走的對象是：', 1, 0, len(members)+1, False, True)
            if (msg):
              index = await findPlayerByNumber(players, msg)
              if (players[index].alive):
                if ((sleep[0] != int(players[index].member.nick)) or (sleep[1])) and (players[index].role != goods[10]) and (int(players[index].member.nick) not in magic):
                  temp_kill.append(int(players[index].member.nick))
                  kills.append(int(players[index].member.nick))
                elif (int(players[index].member.nick) in magic):
                  if (int(players[index].member.nick) == magic[0]):
                    temp_kill.append(magic[1])
                    kills.append(magic[1])
                  else:
                    temp_kill.append(magic[0])
                    kills.append(magic[0])
              else:
                await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
                msg = None
      temp_kill = list(dict.fromkeys(temp_kill))
      temp_kill.sort()
      if (len(temp_kill)):
        for x, kill in enumerate(temp_kill):
          index = await findPlayerByNumber(players, kill)
          players[index].alive = False
          if (int(players[index].member.nick) not in magic_history):
            magic_history.append(int(players[index].member.nick))
            magic_history.sort()
          if (players[index].role in goods):
            if (players[index].role != goods[0]):
              wgc[1] -= 1
            else:
              wgc[2] -= 1
          elif (players[index].role in wolves):
            wgc[0] -= 1
        if (len(temp_kill) != 0):
          msg = ''
          for x, i in enumerate(temp_kill):
            msg += str(i)
            msg += '號'
            if (x != len(temp_kill)-1):
              msg += '、'
          msg += '被殺死！'
          await getMessage(ctx, f'{msg}', False, True, 5, False)
      kills = list(dict.fromkeys(kills))
      kills.sort()
    # 第一日遺言
    if (day == 1):
      for kill in kills:
        await getMessage(ctx, f'{kill}號發表遺言！', False, True, 0, False)
        add = await listenSpeech(ctx, False, speaktime, add, False)
        add = add[0]
    if (no_sheriff[1]):
      continue
    # checking state
    print('---------morning---------')
    for player in players:
      print(f'{player.member}, {player.member.nick}, {player.role}, {player.alive}')
    print(f'{wgc}')
    # 日頭發言
    number = random.randint(1,len(members))
    direction = random.randint(1,2)
    msg = f'{number}號，'
    if (direction == 1):
      msg += '逆向開始發言'
    else:
      msg += '順向開始發言'
    await getMessage(ctx, f'{msg}', False, True, 0, False)
    await getMessage(ctx, '加時輸入\'+\'，自爆輸入\'0\'，使用技能輸入\'s\'，跳過發言輸入任何字元', False, False, 5, False)
    for i in range(sum(wgc)):
      add = await listenSpeech(ctx, False, speaktime, add)
      if (add[1] == 'skill'):
        index = await findPlayerByNumber(players, add[2])
        role = players[index].role
        if (goods[5] == role):
          if (not knight):
            msg = await getNumber(ctx, f'請輸入要撞的對象是：', 1, 0, len(members)+1, False, True, 0, 0)
            if (msg):
              index1 = await findPlayerByNumber(players, msg)
              role1 = players[index1].role
              if (players[index1].alive) and (role1 in wolves):
                await getMessage(ctx, f'{msg}號是狼人，{msg}號淘汰！', False, True, 3, False)
                players[index1].alive = False
                knight = True
                night = True
                add = add[0]
                break
              elif (players[index1].alive):
                await getMessage(ctx, f'{msg}號不是狼人，{players[index].member.nick}號以死謝罪！', False, True, 3, False)
                players[index].alive = False
                knight = True
              else:
                await getMessage(ctx, '請輸入存活的玩家', True, False, 5, False)
                msg = None
          else:
            await getMessage(ctx, '騎士技能已經用過！', False, False, 0, False)
        else:
          await getMessage(ctx, '沒有技能可以使用！', False, False, 0, False)
        add = add[0]
      elif (add[1] == 'explode'):
        index = await findPlayerByNumber(players, add[2])
        players[index].alive = False
        if (players[index].role in goods):
          if (players[index].role != goods[0]):
            wgc[1] -= 1
          else:
            wgc[2] -= 1
        elif (players[index].role in wolves):
          wgc[0] -= 1
        night = True
        add = add[0]
        break
      else:
        add = add[0]
      if (i + 1 != temp_sheriff):
        await getMessage(ctx, '下一位開始發言', True, False, 0, False)
    if (night):
      continue
    # 投票
    if (sheriff):
      await getMessage(ctx, '警長請歸票！', False, True, 0, False)
    await getMessage(ctx, '請用投票功能/自行投出放逐的玩家！', False, False, 0, False)
    msg = await getNumber(ctx, f'請輸入放逐的玩家是：', 1, 0, len(members)+1, True, False, 0, 0, True)
    if (msg[0] in (0, '0', 'e', 'explode', '爆', '自爆')):
      await getMessage(ctx, f'{msg[1]}號自爆！', False, True, 3, False)
      index = await findPlayerByNumber(players, msg[1])
    else:
      await getMessage(ctx, f'{msg[0]}號淘汰，請發表遺言！', False, True, 0, False)
      index = await findPlayerByNumber(players, msg[0])
      add = await listenSpeech(ctx, False, speaktime, add)
      add = add[0]
    players[index].alive = False
    if (players[index].role in goods):
      if (players[index].role != goods[0]):
        wgc[1] -= 1
      else:
        wgc[2] -= 1
    elif (players[index].role in wolves):
      wgc[0] -= 1
    # checking state
    print('----------after----------')
    for player in players:
      print(f'{player.member}, {player.member.nick}, {player.role}, {player.alive}')
    print(f'{wgc}')
  
  # 遊戲結束
  if (not wgc[1] or not wgc[2]):
    await getMessage(ctx, '遊戲結束，狼人獲勝！', False, True, 0, False)
  else:
    await getMessage(ctx, '遊戲結束，好人獲勝！', False, True, 0, False)
  players.sort(key=lambda x: x.member.nick)
  for player in players:
    await getMessage(ctx, f'{player.member.nick}號: {player.role}', False, False, 0, False)

@bot.command(name='exit')
async def _exit(ctx: commands.Context):
  ctx.send('中止遊戲！')

async def getYorN(ctx, q, delete=False, tts=False, delay=0, timeout=0, member=False):
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    if (msg.content.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off', '唔係', '不', '不是', '否')):
      if (member):
        ans = [False, int(msg.author.nick)]
      else:
        ans = False
    elif (msg.content.lower() in ('yes', 'y', 'true', 't', '1', 'enable', 'on', '係', '是')):
      if (member):
        ans = [True, int(msg.author.nick)]
      else:
        ans = True
    else:
      if (delete) and (msg):
        await msg.delete()
      bmsg = await ctx.send('請回答y/n！')
      ans = await getYorN(ctx, q, delete, tts, delay, timeout)
      if (delete) and (bmsg):
        await bmsg.delete()
      return ans
    if (delete) and (msg):
      await msg.delete()
    return ans
  else:
    return msg

async def getLorR(ctx, q, delete=False, tts=False, delay=0, timeout=0):
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    if (msg.content.lower() in ('l', 'left', '左', '左邊', '左面')):
      ans = False
    elif (msg.content.lower() in ('r', 'right', '右', '右邊', '右面')):
      ans = True
    else:
      if (delete) and (msg):
        await msg.delete()
      bmsg = await ctx.send('請回答l/r！')
      ans = await getYorN(ctx, q, delete, tts, delay, timeout)
      if (delete) and (bmsg):
        await bmsg.delete()
      return ans
    if (delete) and (msg):
      await msg.delete()
    return ans
  else:
    return msg

async def getNumber(ctx, q, x=1, min=0, max=100, delete=False, tts=False, delay=0, timeout=0, member=False):
  valid = True
  msg = await getMessage(ctx, q, delete, tts, delay, True, timeout)
  if (msg):
    ans = re.findall(r'\d+', msg.content)
    ans = list(map(int, ans))
    if (len(ans) == x) or ((len(ans) == 1) and (not ans[0])):
      for index in ans:
        if (index not in range(min, max)):
          valid = False
      if (x == 1):
        ans = ans[0]
    else:
      valid = False
    if (member):
      ans = [ans, int(msg.author.nick)]
    if (valid):
      if (delete) and (msg):
        await msg.delete()
      return ans
    else:
      if (delete) and (msg):
        await msg.delete()
      bmsg = await ctx.send(f'請輸入啱的數字！（{min}-{max-1}）')
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

async def listenSpeech(ctx, tts=False, timeout=0, add=[], skill=True):
  if (timeout > 30):
    times = [timeout-30, 30]
  else:
    times = [timeout]
  for x, time in enumerate(times):
    while (time):
      if (len(times) == 1) or (x == 1):
        q = f'{time}秒'
      elif (time < 30):
        q = f'{time+30}秒'
      else:
        q = f'{(time+30)//60}分鐘{(time+30)%60}秒'
      before = datetime.now()
      msg = await getMessage(ctx, q, True, tts, 0, True, time)
      after = datetime.now()
      time -= math.floor((after - before).total_seconds())
      if (msg):
        temp = int(msg.author.nick)
        if (msg.content.lower() in ('0', 'e', 'explode', '爆', '自爆')) and (skill):
          await msg.delete()
          await getMessage(ctx, f'{temp}號自爆！', False, True, 3, False)
          return [add, 'explode', temp]
        elif (msg.content.lower() in ('+', 'add', '加', '加時')):
          await msg.delete()
          if (temp not in add):
            add.append(temp)
            return await listenSpeech(ctx, tts, timeout+time, add)
          else:
            await getMessage(ctx, '已經加過，不能再加！', True, False, 3, False)
        elif (msg.content.lower() in ('s', 'skill')) and (skill):
          await msg.delete()
          return [add, 'skill', temp]
        else:
          await msg.delete()
          msg = await getYorN(ctx, '結束發言，確認？（y/n）', True, False, 0, 0)
          if (msg):
            return [add, 'done']
  msg = await getYorN(ctx, '夠鐘，請問要唔要加時？', True, False, 0, 0, True)
  if (msg[0]):
    if (msg[1] not in add):
      add.append(msg[1])
      return await listenSpeech(ctx, tts, timeout, add)
    else:
      await getMessage(ctx, '已經加過，不能再加！', True, False, 3, False)
      return [add, 'done']
  else:
    return [add, 'done']

async def findPlayerByNumber(players, number):
  for x, player in enumerate(players):
    if (int(player.member.nick) == int(number)):
      return x
  return None

async def findPlayerByRole(players, role):
  for x, player in enumerate(players):
    if (player.role == role):
      return x
  return None

async def setRole(ctx, role, players, x=1):
  authors = await getMember(ctx, f'{role}請輸入任何字元確認身份', True, x, False, 0, 15, [])
  if (authors):
    for author in authors:
      for player in players:
        if (player.member == author):
          player.role = role
    return players
  else:
    return authors

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