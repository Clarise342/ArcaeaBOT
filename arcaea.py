from discord.ext import tasks, commands as cmd
from datetime import datetime as dt
from collections import namedtuple as nt
import discord as dc, json, random, sys, os, asyncio as ao

bot = cmd.Bot(command_prefix="a@")
bot.remove_command("help")

# data settings...
pI = 0 # precence_INDEX
SLs = [None,None,None] # SongList_settings
so = {"ip":[],"l":[],"s":None} # song_option
po = {"ne":"全てが対象","t":[],"s":[]} # partner_option

# song
artworkNT = nt("Artwork", "normal beyond") # artwork
level = nt("Level", "PAST PRESENT FUTURE BEYOND") # レベル
notes = nt("Notes", "PAST PRESENT FUTURE BEYOND") # ノーツ数
constant = nt("Constant", "PAST PRESENT FUTURE BEYOND") # 譜面定数
chart = nt("ChartDesigner", "PAST PRESENT FUTURE BEYOND") # 譜面製作者
song = nt("Song", "name side pack artwork bpm composer artworker chart level notes constant") # song_info

# partner
skill = nt("Skill", "name description awaken") # skill
frag = nt("Frag", "min max awaken") # frag
step = nt("Step", "min max awaken") # step
partner = nt("Partner", "name frag step type skill image") # partner_info

with open("arcaea.json", "r", encoding="utf-8") as f: 
  data = json.load(f) # arcaea_data_add

# to_namedtuple
dataS = list(map(lambda x: song(x[0], x[1], x[2], artworkNT(x[3][0], x[3][1]), x[4], x[5], x[6], chart(x[7][0], x[7][1], x[7][2], x[7][3]), level(x[8][0], x[8][1], x[8][2], x[8][3]), notes(x[9][0],x[9][1],x[9][2],x[9][3]), constant(x[10][0],x[10][1],x[10][2],x[10][3])), data["songs"])) # song
dataPN = list(map(lambda x: partner(x[0], frag(x[1][0], x[1][1], x[1][2]), step(x[2][0], x[2][1], x[2][2]), x[3], skill(x[4][0], x[4][1], x[4][2]), x[5]), data["partners"]["normal"])) # partner_normal
dataPE = list(map(lambda x: partner(x[0], frag(x[1][0], x[1][1], x[1][2]), step(x[2][0], x[2][1], x[2][2]), x[3], skill(x[4][0], x[4][1], x[4][2]), x[5]), data["partners"]["last"])) # partner_event

dataset = [None,None] # data_add

token = os.environ['TOKEN'] # token_read

# setting_dict
main = {"s-ip":2,"s-l":3,"s-s":4,"p-ne":5,"p-t":6,"p-s":7}
dip = {"Ae":"Archive","Aa":"Arcaea","WE":"World Extend","BF":"Black Fate","AP":"Adverse Prelude","LS":"Luminous Sky","VL":"Vicious Labyrinth","EC":"Eternal Core","SR":"Sunset Radiance","AR":"Absolute Reason","BE":"Binary Enfold","AV":"Ambivalent Vision","CS":"Crimson Solace","CM":"CHUNITHM","GC":"Groove Coaster","TS":"Tone Sphere","La":"Lanota","Dx":"Dynamix"} # ignore_packs
dl = {"7":"7","8":"8","9":"9","9+":"9","10":"10","10+":"10+","11":"11"} # levels
dss = {"N":None,"L":"光","C":"対立"} # sides
cne = {"全てが対象":None,"ノーマルのみ":dataPN,"イベントのみ":dataPE}
dne = {"N":"全てが対象","on":"ノーマルのみ","oe":"イベントのみ"} # normal_or_event
dpt = {"B":"バランス","S":"サポート","C":"チャレンジ","?":"???"} # types
dps = {"-":"-","E":"Easy","H":"Hard","V":"Visual","M":"ミラー","O":"オーバーフロー","C":"チュウニズム","A":"Audio"} # skills

# ...settings end

# change_precence
@tasks.loop(minutes=1)
async def loop():
  global pI
  if pI == 0: v = f"Display help with 'a@help'"
  elif pI == 1: v = f"Current ping is {round(bot.latency * 1000)}ms"
  elif pI == 2: v = f"This BOT is developed by Clarice#0920"
  elif pI == 3: v = f"New songs such as Black Fate and World Extend added"   
  elif pI == 4: v = f"a@helpでヘルプを表示します"
  elif pI == 5: v = f"現在のpingは{round(bot.latency * 1000)}msです"
  elif pI == 6: v = f"このBOTの開発者はClarice#0920です"
  elif pI == 7: v = f"Black FateとWorld Extendの楽曲を追加しました"
  await bot.change_presence(activity=dc.Game(name=v))
  pI += 1 if pI != 7 else -7
  
@bot.command()
async def help(ctx):
  await ctx.message.delete()
  e = dc.Embed(title="prefixは `a@` です",color=0x74596d)
  e.timestamp = dt.utcnow()
  e.add_field(name="help",value="ヘルプを表示します",inline=False)
  e.add_field(name="slist <条件>",value="条件に一致する楽曲のリストを表示します",inline=False)
  e.add_field(name="sinfo <曲名>",value="曲の情報を表示します",inline=False)
  e.add_field(name="pinfo <パートナー名>",value="パートナーの情報を表示します",inline=False)
  e.add_field(name="sselect (回数)",value="BOTがランダムに選曲します",inline=False)
  e.add_field(name="pselect",value="BOTがランダムにパートナーを選びます",inline=False)
  e.add_field(name="set",value="設定パネルを表示します",inline=False)
  e.set_author(name="ヘルプ",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  await ctx.send(embed=e,delete_after=60)
  
@bot.command()
async def slist(ctx, *args):
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
  if so["s"] != None: e = dc.Embed(description=sl,color=0x00f1ff) if so["s"] == "光" else dc.Embed(description=sl,color=0x461399)
  else: e = dc.Embed(description=sl,color=0x74596d)
  e.timestamp = dt.utcnow()
  e.set_author(name="楽曲リスト",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  await ctx.send(embed=e,delete_after=60)
  SLs[0], SLs[1], SLs[2] = None, None, None
    
@bot.command()
async def sinfo(ctx, *, name=None):
  await ctx.message.delete()
  if name == None:
    name = dataset[0] if dataset[0] != None else None 
  sgs = [i for i in dataS if name in i.name]
  if len(sgs) == 0: return await ctx.send("曲が見つかりませんでした", delete_after=5.0)
  else: song = sgs[0]
  e = dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x00f1ff) if song.side == "光" else dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x461399)
  e.timestamp = dt.utcnow()
  e.add_field(name="◇ BPM",value=f"{song.bpm}",inline=False)
  e.add_field(name="◇ 作曲者 ・ アートワーク画像作者",value=f"{song.composer} ・ {song.artworker}",inline=False)
  e.add_field(name="◇ 難易度とノーツ数、譜面定数(PST)",value=f"`譜面製作者`: {song.chart.PAST}\n`レベル`: {song.level.PAST}, `譜面定数`: {song.constant.PAST}\n`ノーツ数`: {song.notes.PAST}, `1ノート最高点`: {round(10000000 / int(song.notes.PAST), 3)}",inline=False)
  e.add_field(name="◇ 難易度とノーツ数、譜面定数(PRS)",value=f"`譜面製作者`: {song.chart.PRESENT}\n`レベル`: {song.level.PRESENT}, `譜面定数`: {song.constant.PRESENT}\n`ノーツ数`: {song.notes.PRESENT}, `1ノート最高点`: {round(10000000 / int(song.notes.PRESENT), 3)}",inline=False)
  e.add_field(name="◇ 難易度とノーツ数、譜面定数(FTR)",value=f"`譜面製作者`: {song.chart.FUTURE}\n`レベル`: {song.level.FUTURE}, `譜面定数`: {song.constant.FUTURE}\n`ノーツ数`: {song.notes.FUTURE}, `1ノート最高点`: {round(10000000 / int(song.notes.FUTURE), 3)}",inline=False)
  e.set_author(name="❖ 曲の情報(PST･PRS･FTR) ❖",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  e.set_image(url=song.artwork.normal)
  if song.level.BEYOND != "-":
    b = dc.Embed(title=f"◇ 曲名 {song.name}",description=f"❖ パック {song.pack}",color=0xD00000)
    b.timestamp = dt.utcnow()
    b.add_field(name="❖ BPM",value=f"{song.bpm}",inline=False)
    b.add_field(name="❖ 作曲者 ・ アートワーク画像作者",value=f"{song.composer} ・ {song.artworker}",inline=False)
    b.add_field(name="❖ 難易度とノーツ数、譜面定数(BYD)",value=f"`譜面製作者`: {song.chart.BEYOND}\n`レベル`: {song.level.BEYOND}, `譜面定数`: {song.constant.BEYOND}\n`ノーツ数`: {song.notes.BEYOND}, `1ノート最高点`: {round(10000000 / int(song.notes.BEYOND), 3)}",inline=False)
    b.set_author(name="◆ 曲の情報(BYD) ❖",icon_url=bot.user.avatar_url)
    b.set_footer(text=f"送信者 : {ctx.author.name}")
    b.set_image(url=song.artwork.beyond)
    emojis, embeds, page = ["➡️","⬅️"], [e,b], 0
    m = await ctx.send(embed=embeds[0])
    while not bot.is_closed():
      await m.edit(embed=embeds[page],delete_after=60)
      await m.add_reaction(emojis[page])
      r = await bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and str(r.emoji) in emojis)
      await m.clear_reactions()
      if str(r[0]) == "➡️": page = 1
      else: page = 0
  else:
    await ctx.send(embed=e,delete_after=60)
  
@bot.command()
async def pinfo(ctx, *, name=None):
  await ctx.message.delete()
  if name == None:
    name = dataset[1] if dataset[1] != None else None
  partners = [i for i in dataPN+dataPE if name in i.name]
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
  await ctx.send(embed=e,delete_after=60)
  
@bot.command()
async def sselect(ctx, count=1):
  await ctx.message.delete()
  if count > 10: return await ctx.send("1度に10連続まで可能です", delete_after=5.0)
  enablesP = [i for i in dataS if not i.pack in so["ip"]] if len(so["ip"]) != 0 else dataS
  enablesS = [i for i in enablesP if i.side == so["s"]] if so["s"] != None else enablesP
  enablesL = [i for i in enablesS if i.level.FUTURE in so["l"]] if len(so["l"]) != 0 else enablesS
  if len(enablesL) == 0: return await ctx.send("条件に該当する楽曲が見つかりませんでした", delete_after=5.0)
  results = random.sample(enablesL, count)
  for song in results:
    if song.side == "光": e = dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x00f1ff)
    else: e = dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x461399)
    e.timestamp = dt.utcnow()
    e.set_author(name="❖ 選曲 ❖",icon_url=bot.user.avatar_url)
    e.set_footer(text=f"詳細は a.song_info で確認できます\n送信者 : {ctx.author.name}")
    e.set_thumbnail(url=song.artwork.normal)
    await ctx.send(embed=e)
    dataset[0] = song.name
    
@bot.command()
async def pselect(ctx):
  await ctx.message.delete()
  if cne[po["ne"]] != None: enablesT = [i for i in cne[po["ne"]] if i.type in po["t"]] if len(po["t"]) != 0 else cne[po["ne"]]
  else: enablesT = [i for i in dataPN+dataPE if i.type in po["t"]] if len(po["t"]) != 0 else dataPN+dataPE
  enablesS = [i for i in enablesT if i.skill.name in po["s"]] if len(po["s"]) != 0 else enablesT
  if len(enablesS) == 0: return await ctx.send("条件に該当するパートナーが見つかりませんでした", delete_after=5.0)
  result = enablesS[random.randint(0,len(enablesS)-1)]
  e = dc.Embed(title=f"◆ パートナー名 {result.name}",description=f"◇ タイプ {result.type}",color=0x74596d)
  e.timestamp = dt.utcnow()
  e.set_author(name="❖ パートナー選択 ❖",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"詳細は a.partner_info で確認できます\n送信者 : {ctx.author.name}")
  await ctx.send(embed=e)
  dataset[1] = result.name 
  
@bot.command(name="set")
async def setting(ctx):
  await ctx.message.delete()
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
        if m.content == "x": return await msg.delete()
        elif m.content == "ns":
          Sip = ' '.join(so["ip"]) + "を除外" if len(so["ip"]) > 0 else "なし"
          Sl = ' '.join(so["l"]) + "のみ" if len(so["l"]) > 0 else "全て"
          Pt = ' '.join(po["t"]) + "のみ" if len(po["t"]) > 0 else "全て"
          Ps = ' '.join(po["s"]) + "のみ" if len(po["s"]) > 0 else "全て"
          if po["ne"] == None: Pne = "全てが対象"
          else: Pne = "ノーマルのみ" if po["ne"] == dataPN else "イベントのみ"
          ns = dc.Embed(color=0x74596d)
          ns.timestamp = dt.utcnow()
          ns.add_field(name="**◇ 楽曲セレクト ◇**",value=f"・除外パック: {Sip}\n・レベル: {Sl}\n・サイド: {so['s']}",inline=False)
          ns.add_field(name="**◇ パートナーセレクト ◇**",value=f"・セレクト対象: {Pne}\n・タイプ: {Pt}\n・スキル: {Ps}",inline=False)
          ns.set_author(name="現在の設定",icon_url=bot.user.avatar_url)
          ns.set_footer(text=f"送信者 : {ctx.author.name}")
          es[1], p = ns, 1
        elif m.content in main: p = main[m.content]
        else: pass
      elif p == 1:
        if m.content in ["back","b"]: p = 0
        else: pass
      else:
        if p == 2:
          if m.content in dip:
            if dip[m.content] in so["ip"]: del so["ip"][so["ip"].index(dip[m.content])]
            else: so["ip"].append(dip[m.content])
          else: pass
        elif p == 3:
          if m.content in dl:
            if dl[m.content] in so["l"]: del so["l"][so["l"].index(dl[m.content])]
            else: so["l"].append(dl[m.content])      
          else: pass
        elif p == 4:
          if m.content in dss: so["s"] = dss[m.content]
          else: pass
        elif p == 5:
          if m.content in dne: po["ne"] = dne[m.content]
          else: pass
        elif p == 6:
          if m.content in dpt:
            if dpt[m.content] in po["t"]: del po["t"][po["t"].index(dpt[m.content])]
            else: po["t"].append(dpt[m.content])              
          else: pass
        elif p == 7:
          if m.content in dps:
            if dps[m.content] in po["s"]: del po["s"][po["s"].index(dps[m.content])]
            else: po["s"].append(dps[m.content])              
          else: pass
        p = 0
    except ao.TimeoutError: return await msg.delete()
 
@bot.event
async def on_ready():
  sn = dc.Embed(title="ArcaeaBOTが起動しました",color=0xBCF946)
  sn.timestamp = dt.utcnow()
  sn.set_author(name="起動通知",icon_url=bot.user.avatar_url)
  sn.set_footer(text="Powered by Python (3.7)")
  ch = bot.get_channel(723600070284673036)
  await ch.send(embed=sn)
  print("起動しました")
  loop.start()
                      
@bot.event
async def on_reaction_add(reaction, user):
  if reaction.emoji.id == 723169353423519834:
    await reaction.message.delete()
                  
@bot.event
async def on_message(message):
  if message.author.id == 558181877819768843:
    await message.delete()
                       
bot.add_listener(on_message)
bot.run(token)
