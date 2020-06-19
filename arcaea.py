from discord.ext import tasks, commands as cmd
from datetime import datetime as dt
from collections import namedtuple as nt
import discord as dc, json, random, sys, os, asyncio as ao

bot = cmd.Bot(command_prefix="a")
bot.remove_command("help")

# data settings...

pI = 0 # precence_INDEX

SLs = [None,None,None] # SongList_settings

so = {"ip":[],"l":[],"s":None} # song_option
po = {"n":None,"t":[],"s":[]} # partner_option

# song
artworkNT = namedtuple("Artwork", "normal beyond") # artwork
level = namedtuple("Level", "PAST PRESENT FUTURE BEYOND") # levels
notes = namedtuple("Notes", "PAST PRESENT FUTURE BEYOND") # notes
song = namedtuple("Song", "name side pack artwork bpm composer level notes") # song_info

# partner
skill = namedtuple("Skill", "name description awaken") # skill
frag = namedtuple("Frag", "min max awaken") # frag
step = namedtuple("Step", "min max awaken") # step
partner = namedtuple("Partner", "name frag step type skill image") # partner_info

with open("arcaea.json", "r", encoding="utf-8") as f: 
  data = json.load(f) # arcaea_data_add

# to_namedtuple
dataS = list(map(lambda x: song(x[0], x[1], x[2], artworkNT(x[3][0], x[3][1]), x[4], x[5], level(x[6][0], x[6][1], x[6][2], x[6][3]), notes(x[7][0],x[7][1],x[7][2],x[7][3])), data["songs"])) # song
dataPN = list(map(lambda x: partner(x[0], frag(x[1][0], x[1][1], x[1][2]), step(x[2][0], x[2][1], x[2][2]), x[3], skill(x[4][0], x[4][1], x[4][2]), x[5]), data["partners"]["normal"])) # partner_normal
dataPE = list(map(lambda x: partner(x[0], frag(x[1][0], x[1][1], x[1][2]), step(x[2][0], x[2][1], x[2][2]), x[3], skill(x[4][0], x[4][1], x[4][2]), x[5]), data["partners"]["last"])) # partner_event

dataset = [None,None] # data_add

# setting_dict
dip = {"Ae":"Archive","Aa":"Arcaea","WE":"World Extend","BF":"Black Fate","AP":"Adverse Prelude","LS":"Luminous Sky","VL":"Vicious Labyrinth","EC":"Eternal Core","SR":"Sunset Radiance","AR":"Absolute Reason","BE":"Binary Enfold","AV":"Ambivalent Vision","CS":"Crimson Solace","CM":"CHUNITHM","GC":"Groove Coaster","TS":"Tone Sphere","La":"Lanota","Dx":"Dynamix"} # ignore_packs
dl = {"6":"6","7":"7","8":"8","9":"9","9+":"9","10":"10","10+":"10+","11":"11"} # levels
dss = {"N":None,"L":dataPN,"C":dataPE} # sides
dne = {"N":"なし","on":"ノーマルのみ","oe":"イベントのみ"} # normal_or_event
dt = {"B":"バランス","S":"サポート","C":"チャレンジ","?":"???"} # types
dps = {"-":"-","E":"Easy","H":"Hard","V":"Visual","M":"ミラー","O":"オーバーフロー","C":"チュウニズム","A":"Audio"} # skills
dne = {None:"なし",dataPN:"光のみ",dataPE:"対立のみ"} # setting_name

# ...settings end

# change_precence
@tasks.loop(seconds=30)
async def loop():
  global pI
  if pI == 0: v = f"Display help with 'a.help (a.h)'"
  elif pI == 1: v = f"Current ping is {round(bot.latency * 1000)}ms"
  elif pI == 2: v = f"This BOT is developed by Clarice#0920"
  elif pI == 3: v = f"New songs such as Black Fate and World Extend added"
  await bot.change_presence(activity=dc.Game(name=value))
  pI += 1 if pI != 3 else -3
  
@bot.command(aliases=["h"])
async def help(ctx):
  e = dc.Embed(color=0x74596d)
  e.timestamp = dt.utcnow()
  e.add_field(name="help",value="ヘルプを表示します",inline=False)
  e.add_field(name="sinfo <曲名>",value="曲の情報を表示します",inline=False)
  e.add_field(name="pinfo <パートナー名>",value="パートナーの情報を表示します",inline=False)
  e.add_field(name="sselect (回数)",value="BOTがランダムに選曲します",inline=False)
  e.add_field(name="pselect",value="BOTがランダムにパートナーを選びます",inline=False)
  e.add_field(name="set",value="設定パネルを表示します",inline=False)
  e.set_author(name="ヘルプ",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  await ctx.send(embed=e)
  
@bot.command(aliases=["sl"])
async def song_list(ctx, *args):
  await ctx.message.delete()
  if "/p" in args:
    if "\\p" in args: SLs[0] = args[args.index("/p")+1:args.index("\\p")]
    else: SLs[0] = args[args.index("/p")+1:args.index("/p")+2]
  if "/s" in args: SLs[1] = args[args.index("/s")+1]
  if "/l" in args:
    if "\\l" in args: SLs[2] = args[args.index("/l")+1:args.index("\\l")]
    else: SLs[2] = args[args.index("/l")+1:args.index("/l")+2]
  listsP = [i for i in dataS if not i.pack in SLs[0]] if SLs[0] != None else dataS
  listsS = [i for i in listsP if i.side == SLs[1]] if SLs[1] != None else listsP
  listsL = [i.name for i in listsS if i.level.FUTURE in SLs[2]] if SLs[2] != None else [i.name for i in listsS]
  sl = '\n'.join(listsL)
  if so["s"] != None: e = dc.Embed(description=sl,color=0x00f1ff) if so["s"] == "光" else discord.Embed(description=sl,color=0x461399)
  else: e = discord.Embed(description=sl,color=0x74596d)
  e.timestamp = dt.utcnow()
  e.set_author(name="楽曲リスト",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  await ctx.send(embed=e)
  SLs[0], SLs[1], SLs[2] = None, None, None
    
@bot.command(aliases=["si"])
async def sinfo(ctx, *, name=None):
  if name == None:
    name = dataset[0] if dataset[0] != None else None 
  sgs = [i for i in dataS if name in i.name]
  if len(songs) == 0: return await ctx.send("曲が見つかりませんでした", delete_after=5.0)
  else: song = sgs[0]
  e = dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x00f1ff) if song.side == "光" else dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x461399)
  e.timestamp = dt.utcnow()
  e.add_field(name="◇ BPM",value=f"{song.bpm}",inline=False)
  e.add_field(name="◇ 作曲者",value=f"{song.composer}",inline=False)
  e.add_field(name="◇ 難易度とノーツ数(PAST)",value=f"{song.level.PAST} | {song.notes.PAST}\n1ノート最高点 {round(10000000 / int(song.notes.PAST), 3)}",inline=False)
  e.add_field(name="◇ 難易度とノーツ数(PRESENT)",value=f"{song.level.PRESENT} | {song.notes.PRESENT}\n1ノート最高点 {round(10000000 / int(song.notes.PRESENT), 3)}",inline=False)
  e.add_field(name="◇ 難易度とノーツ数(FUTURE)",value=f"{song.level.FUTURE} | {song.notes.FUTURE}\n1ノート最高点 {round(10000000 / int(song.notes.FUTURE), 3)}",inline=False)
  e.set_author(name="❖ 曲の情報(PST･PRS･FTR) ❖",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  e.set_image(url=song.artwork.normal)
  if song.level.BEYOND != "-":
    b = dc.Embed(title=f"◇ 曲名 {song.name}",description=f"❖ パック {song.pack}",color=0xD00000)
    b.timestamp = dt.utcnow()
    b.add_field(name="❖ BPM",value=f"{song.bpm}",inline=False)
    b.add_field(name="❖ 作曲者",value=f"{song.composer}",inline=False)
    b.add_field(name="❖ 難易度とノーツ数(BEYOND)",value=f"{song.level.BEYOND} | {song.notes.BEYOND}\n1ノート最高点 {round(10000000 / int(song.notes.BEYOND), 3)}",inline=False)
    b.set_author(name="◆ 曲の情報(BYD) ❖",icon_url=bot.user.avatar_url)
    b.set_footer(text=f"送信者 : {ctx.author.name}")
    b.set_image(url=song.artwork.beyond)
    emojis, embeds, page = ["➡️","⬅️"], [e,b], 0
    m = await ctx.send(embed=embeds[0])
    while not bot.is_closed():
      await m.edit(embed=embeds[page])
      await m.add_reaction(emojis[page])
      r = await bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and str(r.emoji) in emojis)
      await m.clear_reactions()
      if str(r[0]) == "➡️": page = 1
      else: page = 0
  else:
    await ctx.send(embed=e)
  
@bot.command(aliases=["pi"])
async def pinfo(ctx, *, name=None):
  if name == None:
    name = dataset[1] if dataset[1] != None else None 
  partners = [i for i in dataPN if name in i.name]
  if len(partners) == 0: partners = [i for i in dataPE if name in i.name]
  if len(partners) == 0: return await ctx.send("パートナーが見つかりませんでした", delete_after=5.0)
  partner = partners[0]
  e = dc.Embed(title=f"◆ パートナー名 {partner.name}",description=f"◇ タイプ {partner.type}",color=0x74596d)
  e.timestamp = dt.utcnow()
  e.add_field(name="◇ FragとStep(最小値)",value=f"{partner.frag.min} | {partner.step.min}",inline=False)
  e.add_field(name="◇ FragとStep(最大値)",value=f"{partner.frag.max} | {partner.step.max}",inline=False)
  e.add_field(name="◇ FragとStep(覚醒後)",value=f"{partner.frag.awaken} | {partner.step.awaken}",inline=False)
  e.add_field(name=f"◇ Skill ({partner.skill.name})",value=f"{partner.skill.description}\n(覚醒後: {partner.skill.awaken})",inline=False)
  e.set_author(name="❖ パートナーの情報 ❖",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  e.set_image(url=partner.image)
  await ctx.send(embed=e)
  
@bot.command(aliases=["ss"])
async def sselect(ctx, count=1):
  if count > 10: return await ctx.send("1度に10連続まで可能です", delete_after=5.0)
  enables_p = [i for i in data_s if not i.pack in so["ep"]] if len(so["ep"]) != 0 else data_s
  enables_s = [i for i in enables_p if i.side == so["s"]] if so["s"] != None else enables_p
  enables_l = [i for i in enables_s if i.level.FUTURE in so["l"]] if len(so["l"]) != 0 else enables_s
  if len(enables_l) == 0: return await ctx.send("条件に該当する楽曲が見つかりませんでした", delete_after=5.0)
  results = random.sample(enables_l, count)
  for song in results:
    if song.side == "光": e = discord.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x00f1ff)
    else: e = discord.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x461399)
    e.timestamp = dt.utcnow()
    e.set_author(name="❖ 選曲 ❖",icon_url=bot.user.avatar_url)
    e.set_footer(text=f"詳細は a.song_info で確認できます\n送信者 : {ctx.author.name}")
    e.set_thumbnail(url=song.artwork.normal)
    await ctx.send(embed=e)
    data_set[0] = song.name
    
@bot.command(aliases=["ps"])
async def pselect(ctx):
  if po["nl"] != None: enables_t = [i for i in po["nl"] if i.type in po["t"]] if len(po["t"]) != 0 else data_p_n
  else: enables_t = [i for i in data_p_n.extend(data_p_l) if i.type in po["t"]] if len(po["t"]) != 0 else data_p_l
  enables_s = [i for i in enables_t if i.skill.name in po["s"]] if len(po["t"]) != 0 else enables_t
  if len(enables_s) == 0: return await ctx.send("条件に該当するパートナーが見つかりませんでした", delete_after=5.0)
  result = enables_s[random.randint(0,len(enables_s)-1)]
  e = discord.Embed(title=f"◆ パートナー名 {result.name}",description=f"◇ タイプ {result.type}",color=0x74596d)
  e.set_author(name="❖ パートナー選択 ❖",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"詳細は a.partner_info で確認できます\n送信者 : {ctx.author.name}")
  await ctx.send(embed=e)
  data_set[1] = result.name 
  
@bot.command(name="set",aliases=["s"])
async def setting(ctx):
  mp = dc.Embed(title="操作を以下から選んで下さい",description="`x`: 終了\n`ns`: 現在の設定を確認\n`s-ip`: 選曲 | 除外パック\n`s-l`: 選曲 | レベル\n`s-s`: 選曲 | サイド\n`p-ne`: パートナー | ノーマル/イベント\n`p-t`: パートナー | タイプ\n`p-s`: パートナー | スキル",color=0x74596d)
  ip = dc.Embed(title="以下から除外、追加するパックを選択してください",description="`Ae`: Archive\n`Aa`: Arcaea\n`WE`: World Extend\n`BF`: Black Fate\n`AP`: Adverse Prelude\n`LS`: Luminous Sky\n`VL`: Vicious Labyrinth\n`EC`: Eternal Core\n`SR`: Sunset Radiance\n`AR`: Absolute Reason\n`BE`: Binary Enfold\n`AV`: Ambivalent Vision\n`CS`: Crimson Solace\n`CM`: CHUNITHM\n`GC`: Groove Coaster\n`TS`: Tone Sphere\n`La`: Lanota\n`Dx`: Dynamix",color=0x74596d)
  l = dc.Embed(title="以下から追加、除外する難易度を選択してください",description="`6`: 6\n`7`: 7\n`8`: 8\n`9`: 9\n`9+`: 9+\n`10`: 10\n`10+`: 10+\n`11`: 11",color=0x74596d)
  ss = dc.Embed(title="以下からサイドを選択してください",description="`N`: なし\n`L`: 光のみ\n`C`: 対立のみ",color=0x74596d)
  ne = dc.Embed(title="以下から選択してください",description="`N`: なし\n`on`: ノーマルのみ\n`oe`: イベントのみ",color=0x74596d)
  t = dc.Embed(title="以下から追加、除外するタイプを選択してください",description="`B`: バランス\n`S`: サポート\n`C`: チャレンジ\n`?`: ???",color=0x74596d)
  ps = dc.Embed(title="以下から追加、除外するスキルを選択してください",description="`-`: -\n`E`: Easy\n`H`: Hard\n`V`: Visual\n`M`: ミラー\n`O`: オーバーフロー\n`C`: チュウニズム\n`A`: Audio",color=0x74596d)
  p, es = 0, [mp, None, ip, l, ss, ne, t, ps]
  msg = await ctx.send(embed=es[p])
  while not bot.is_closed():
    await msg.edit(embed=es[p])
    try:
      m = await bot.wait_for('message', timeout=40.0, check=lambda m: ctx.author == m.author)
      await m.delete()
      if p == 0:
        if m == "x": return await msg.delete()
        if m == "ns":
          Sip = ' '.join(so["ip"]) + "を除外" if len(so["ip"]) > 0 else "なし"
          Sl = ' '.join(so["l"]) + "のみ" if len(so["l"]) > 0 else "全て"
          Pt = ' '.join(po["t"]) + "のみ" if len(po["t"]) > 0 else "全て"
          Ps = ' '.join(po["s"]) + "のみ" if len(po["s"]) > 0 else "全て"
          Pn = 
          ns = dc.Embed(title="現在の設定はこちらです",description="**◇ ",color=0x74596d)
      if p == 1:
        
    except ao.TimeoutError: return await msg.delete()
      
@bot.command(aliases=["e"])
async def exit(ctx):
  print("終了しました")
  await ctx.message.delete()
  await bot.logout()
  await sys.exit()
  
@bot.event
async def on_ready():
  print("起動しました")
  loop.start()
  
bot.run("NzAyNTg3MzI0NzE4MTIwOTkx.XsZY1g.ZDRqveB5TxdBKKtDC3zjED7nywc")
    