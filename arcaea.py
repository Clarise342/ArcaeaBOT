from discord.ext import tasks, commands as cmd
from datetime import datetime as dt
from collections import namedtuple as nt
import discord as dc, json, random, sys, os, asyncio as ao

bot = cmd.Bot(command_prefix="a@")
bot.remove_command("help")

# 設定
pindex = 0 # ステータス番号
slset = [None,None,None] # "slist"での絞り込み
sopt = {"ignorepacks":[],"ignoresongs":[],"levels":[],"side":None,"illustrators":[],"composers":[],"chart_creators":[]"notes_limit":[0,1600],"constant_limit":[1.0,12.0]} # "sselect"での絞り込み
popt = {"resident":"全てが対象","step_limit":[0,200],"frag_limit":[0,200],"types":[],"skills":[]} # "pselect"での絞り込み

# 楽曲関連
artwork_nt = nt("Artwork", "normal beyond") # artwork
level_nt = nt("Level", "PAST PRESENT FUTURE BEYOND") # レベル
notes_nt = nt("Notes", "PAST PRESENT FUTURE BEYOND") # ノーツ数
constant_nt = nt("Constant", "PAST PRESENT FUTURE BEYOND") # 譜面定数
chart_nt = nt("ChartDesigner", "PAST PRESENT FUTURE BEYOND") # 譜面製作者
tags_nt = nt("Tags", "composer illustrator chartdesigner")
song_nt = nt("Song", "name side pack artwork bpm composer illustrator chart tags level notes constant") # song_info

# パートナー関連
skill_nt = nt("Skill", "name description awaken") # skill
frag_nt = nt("Frag", "min max awaken") # frag
step_nt = nt("Step", "min max awaken") # step
partner_nt = nt("Partner", "name resident frag step type skill image") # partner_info

with open("arcaea.json", "r", encoding="utf-8") as f: 
  data = json.load(f) # 情報読み込み

# namedtupleに変換
sdata = list(map(lambda x: song_nt(x[0], x[1], x[2], artwork_nt(x[3][0], x[3][1]), x[4], x[5], x[6], chart_nt(x[7][0], x[7][1], x[7][2], x[7][3]), tags_nt(x[8][0], x[8][1], x[8][2]), level_nt(x[9][0], x[9][1], x[9][2], x[9][3]), notes_nt(x[10][0],x[10][1],x[10][2],x[10][3]), constant_nt(x[11][0],x[11][1],x[11][2],x[11][3])), data["songs"])) # song
pdata = list(map(lambda x: partner_nt(x[0], x[1], frag_nt(x[2][0], x[2][1], x[2][2]), step_nt(x[3][0], x[3][1], x[3][2]), x[4], skill_nt(x[5][0], x[5][1], x[5][2]), x[6]), data["partners"])) # partner_normal

dataset = [None,None] # 臨時保存

token = os.environ['TOKEN'] # トークン読み込み

# 設定に対する内容辞典
first = {"s-ip":2,"s-l":3,"s-s":4,"p-ne":5,"p-t":6,"p-s":7}
ignorepacks = {"Ae":"Archive","Aa":"Arcaea","WE":"World Extend","BF":"Black Fate","AP":"Adverse Prelude","LS":"Luminous Sky","VL":"Vicious Labyrinth","EC":"Eternal Core","SR":"Sunset Radiance","AR":"Absolute Reason","BE":"Binary Enfold","AV":"Ambivalent Vision","CS":"Crimson Solace","CM":"CHUNITHM","GC":"Groove Coaster","TS":"Tone Sphere","La":"Lanota","Dx":"Dynamix"} # ignore_packs
sides = {"all":None,"light":"光","conflict":"対立"} # side
composers = ['T2Kazuya', 'chitose', 'a-zu-ra', '南ゆ に', 'Sound Souler', 'U-ske', 'lueur', 'Tiny Minim', 'Frums', 'HyuN', '旅人E', 'REDSHiFT', 'Blacklolita', 'しーけー', 'Arch', 'n3pu', 'ARForest', 'Iris', 'gmtn.', 'Missionary', 'DIA', 'Aire', 'ak+q', 'WHITEFISTS', 'Sakuzyo', 'Jun Kuroda', 'Farhan', 'Kolaa', 'Puru', 'THB', 'Sta', 'sky_delta', '翡野イスカ', 'お月さま交響曲', 'Rabbit House', 'Ryazan', 'Combatplayer', 'Soleily', 'Yooh', 'void', 'cYsmix', 'wa.', 'DJ Myosuke', '7mai', '3R2', 'Cosmograph', 'Mameyudoufu', 'uno', 'ちょこ', 'Silentroom', 'アリスシャッハと魔法の楽団', 'REDALiCE', 'siromaru', 't+pazolite', 'TQ☆', 'ikaruga_nex', 'Feryquitous', 'Sennzai', 'MYTK', 'Ras', 'BACO', '溝口ゆうま', '大瀬良あい', 'WHITEFIST', 'からとpαnchii少年', 'はるの', 'MYUKKE.', 'ginkiha', 'Sampling Masters MEGA', 'TANO*C Sound Team', 'USAO', 'DJ Genki', 'DJ Noriken', 'P*Light', 't*pazolite', '黒皇帝', 'Laur', 'Street', 'Maozon', 'Noah', '光吉猛修', 'Zekk', 'Apo11o program', 'ETIA.', 'HiTECH NINJA', 'Saiph', 'Virtual Self', 'HATE', 'Junk', 'Mitomoro', 'Mili', 'PSYQUI', 'Nitro', 'Missive New Krew', 'かゆき', 'Hyun', 'Syepias', 'jioyi', 'Tanchiky', 'xi', 'nora2r', 'Gram', 'YUKIYANAGI', 'Nhato', 'EBIMAYO', 'Yamajet', 'Powerless', 'Aoi', 'siqlo', 'モリモリあつし', 'Yunosuke', 'MASAKI', 'ぺのれり', 'Kobaryo', 'WAiKURO', 'Cranky', 'cybermiso', '翡乃イ スカ', 'uma', 'LeaF', 'Polysha', '橘花音', 'Akira Complex', 'Juggernaut.', 'A.SAKA', 'Team Grimoire', 'かめりあ(EDP)', 'Edelritter']
illustrators = ['T2Kazuya', 'Khronetic', '不明', '白鳥怜', 'ましろみ のあ', '橙乃遥', 'Hanamori Hiro', 'Tagtraume', 'NanoKun', '黒刃愛', 'grosspanda', '釜飯轟々丸', 'かぐやのもちづき', 'yoshimo', 'Shionty', 'RiceGnat', 'Ancy', '雨風雪夏', 'Mechari', 'terry', 'nakanome', 'レアル', 'Saga', 'キッカイキ', 'mins', 'Frums', 'VMWT', 'シエラ', 'deronoitz', 'Megu', 'お月さま交響曲', 'YEONIE', '織日ちひろ', 'Doomfest', 'CinEraLiA', '八葉', 'Koyama Mai', 'Eric Dagley', '百舌谷', 'トロ3', 'Refla', 'BerryVerrine', 'Photonskyto', 'DJ Poyoshi', 'unKn', ' アリスシャッハと魔法の楽団', 'nonokuro', '駿', 'HenryTz', '出前', '魔界の住人', '未早', 'softmode', 'kobuta', 'ふぇいフリック', 'SiNoe', 'LAM', 'Sta', 'NTFS', '巻羊', 'mokeo', 'fixro2n', 'rtil', '和音ハカ', 'wacca', 'hideo', 'yusi.', 'クルエルGZ', ' スズカミ', 'そゐち', '久賀フーナ', 'Hie', 'mirimo', 'iimo', 'すずなし', 'きらばがに', 'Sou', 'SKT', 'アサヤ', '吠L', 'EB十', '姐川', 'リウイチ', '岩十', 'horte', 'deel', 'GreeN', 'SERXPHIS', 'Rolua', 'NAGU', '望月けい', 'KEI']
chart_creators = ['Nitro', 'Toaster', 'Kurorak', 'k//eternal', '-chartaesthesia-', 'TaroNuke', '石樂', 'Exschwation', 'Black Tea', 'Arcaea Team', '緑', 'CERiNG', 'Kero', 'Darkest Dream', '不明', '/', 'Arcaea Charting Team', 'The Monolith', 'Zero Sky', 'Paradox', '迷路', 'Tempest']
display_resident = {"all":"全てのパートナーを含みます","normal":"現在入手可能なパートナーのみを含みます","event":"イベントでのみ入手可能なパートナーのみを含みます"} # 常駐絞り込み
types = {"B":"バランス","S":"サポート","C":"チャレンジ","?":"???"} # types
skills = {"-":"-","E":"Easy","H":"Hard","V":"Visual","M":"ミラー","O":"オーバーフロー","C":"チュウニズム","A":"Audio"} # skills

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
    if dataset[0] != None: name = dataset[0]
    else: await ctx.send("曲名を入力して下さい")
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
  l = dc.Embed(title="以下から追加、除外する難易度を選択してください",description="`7`: 7\n`8`: 8\n`9`: 9\n`9+`: 9+\n`10`: 10\n`10+`: 10+\n`11`: 11",color=0x74596d)
  ss = dc.Embed(title="以下から絞り込むサイドを選択してください",description="`all`: 全て\n`light`: 光のみ\n`conflict`: 対立のみ",color=0x74596d)
  ne = dc.Embed(title="以下から選択してください",description="`all`: 全て\n`normal`: ノーマルのみ\n`event`: イベントのみ",color=0x74596d)
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
          if m.content in ignorepacks:
            if ignorepacks[m.content] in so["ip"]: del so["ip"][so["ip"].index(dip[m.content])]
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
  if type(reaction.emoji) != str: 
    if reaction.emoji.id == 723169353423519834:
      await reaction.message.delete()
                                          
bot.run(token)
