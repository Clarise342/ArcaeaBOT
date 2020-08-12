from discord.ext import tasks, commands as cmd
from datetime import datetime as dt
from collections import namedtuple as nt
import discord as dc, json, random, sys, os, asyncio as ao

bot = cmd.Bot(command_prefix="a-")
bot.remove_command("help")

# 設定
pindex = 0 # ステータス番号
	
sopt = {
    "ignorepacks":[],
    "ignoresongs":[],
    "levels":[
    [],
    [],
    [],
    []
  ],
  "side":None,
  "illustrators":[],
  "composers":[],
  "chart_creators":[],
  "notes_limit":[
    [0,1600],
    [0,1600],
    [0,1600],
    [0,1600]
  ],
  "constant_limit":[
    [1.0,12.0],
    [1.0,12.0],
    [1.0,12.0],
    [1.0,12.0]
  ]
}

popt = {
  "resident":"all",
  "step_limit":[
    [0,200],
    [0,200]
  ],
  "frag_limit":[
    [0,200],
    [0,200]
  ],
  "types":[],
  "skills":[]
}

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
sfirst = {"ip":2,"is":3,"l":4,"s":9,"nl":10,"cl":15,"co":20,"il":21,"ch":22}
pfirst = {"r":24,"t":25,"s":26,"fl":27,"sl":30}
ignorepacks = {"Ae":"Archive","Aa":"Arcaea","WE":"World Extend","BF":"Black Fate","AP":"Adverse Prelude","LS":"Luminous Sky","VL":"Vicious Labyrinth","EC":"Eternal Core","SR":"Sunset Radiance","AR":"Absolute Reason","BE":"Binary Enfold","Am":"Ambivalent Vision","CS":"Crimson Solace","CH":"CHUNITHM","GC":"Groove Coaster","TS":"Tone Sphere","La":"Lanota","Dx":"Dynamix"} # ignore_packs
sides = {"all":None,"light":"光","conflict":"対立"} # side
composers = ['T2Kazuya', 'chitose', 'a-zu-ra', '南ゆに', 'Sound Souler', 'U-ske', 'lueur', 'Tiny Minim', 'Frums', 'HyuN', '旅人E', 'REDSHiFT', 'Blacklolita', 'しーけー', 'Arch', 'n3pu', 'ARForest', 'Iris', 'gmtn.', 'Missionary', 'DIA', 'Aire', 'ak+q', 'WHITEFISTS', 'Sakuzyo', 'Jun Kuroda', 'Farhan', 'Kolaa', 'Puru', 'THB', 'Sta', 'sky_delta', '翡野イスカ', 'お月さま交響曲', 'Rabbit House', 'Ryazan', 'Combatplayer', 'Soleily', 'Yooh', 'void', 'cYsmix', 'wa.', 'DJ Myosuke', '7mai', '3R2', 'Cosmograph', 'Mameyudoufu', 'uno', 'ちょこ', 'Silentroom', 'アリスシャッハと魔法の楽団', 'REDALiCE', 'siromaru', 't+pazolite', 'TQ☆', 'ikaruga_nex', 'Feryquitous', 'Sennzai', 'MYTK', 'Ras', 'BACO', '溝口ゆうま', '大瀬良あい', 'WHITEFIST', 'からとpαnchii少年', 'はるの', 'MYUKKE.', 'ginkiha', 'Sampling Masters MEGA', 'TANO*C Sound Team', 'USAO', 'DJ Genki', 'DJ Noriken', 'P*Light', 't*pazolite', '黒皇帝', 'Laur', 'Street', 'Maozon', 'Noah', '光吉猛修', 'Zekk', 'Apo11o program', 'ETIA.', 'HiTECH NINJA', 'Saiph', 'Virtual Self', 'HATE', 'Junk', 'Mitomoro', 'Mili', 'PSYQUI', 'Nitro', 'Missive New Krew', 'かゆき', 'Hyun', 'Syepias', 'jioyi', 'Tanchiky', 'xi', 'nora2r', 'Gram', 'YUKIYANAGI', 'Nhato', 'EBIMAYO', 'Yamajet', 'Powerless', 'Aoi', 'siqlo', 'モリモリあつし', 'Yunosuke', 'MASAKI', 'ぺのれり', 'Kobaryo', 'WAiKURO', 'Cranky', 'cybermiso', '翡乃イスカ', 'uma', 'LeaF', 'Polysha', '橘花音', 'Akira Complex', 'Juggernaut.', 'A.SAKA', 'Team Grimoire', 'かめりあ(EDP)', 'Edelritter']
illustrators = ['T2Kazuya', 'Khronetic', '不明', '白鳥怜', 'ましろみ のあ', '橙乃遥', 'Hanamori Hiro', 'Tagtraume', 'NanoKun', '黒刃愛', 'grosspanda', '釜飯轟々丸', 'かぐやのもちづき', 'yoshimo', 'Shionty', 'RiceGnat', 'Ancy', '雨風雪夏', 'Mechari', 'terry', 'nakanome', 'レアル', 'Saga', 'キッカイキ', 'mins', 'Frums', 'VMWT', 'シエラ', 'deronoitz', 'Megu', 'お月さま交響曲', 'YEONIE', '織日ちひろ', 'Doomfest', 'CinEraLiA', '八葉', 'Koyama Mai', 'Eric Dagley', '百舌谷', 'トロ3', 'Refla', 'BerryVerrine', 'Photonskyto', 'DJ Poyoshi', 'unKn', 'アリスシャッハと魔法の楽団', 'nonokuro', '駿', 'HenryTz', '出前', '魔界の住人', '未早', 'softmode', 'kobuta', 'ふぇいフリック', 'SiNoe', 'LAM', 'Sta', 'NTFS', '巻羊', 'mokeo', 'fixro2n', 'rtil', '和音ハカ', 'wacca', 'hideo', 'yusi.', 'クルエルGZ', ' スズカミ', 'そゐち', '久賀フーナ', 'Hie', 'mirimo', 'iimo', 'すずなし', 'きらばがに', 'Sou', 'SKT', 'アサヤ', '吠L', 'EB十', '姐川', 'リウイチ', '岩十', 'horte', 'deel', 'GreeN', 'SERXPHIS', 'Rolua', 'NAGU', '望月けい', 'KEI']
chart_creators = ['Nitro', 'Toaster', 'Kurorak', 'k//eternal', '-chartaesthesia-', 'TaroNuke', '石樂', 'Exschwation', 'Black Tea', 'Arcaea Team', '緑', 'CERiNG', 'Kero', 'Darkest Dream', '不明', '/', 'Arcaea Charting Team', 'The Monolith', 'Zero Sky', 'Paradox', '迷路', 'Tempest']
display_resident = {"all":"全てのパートナーを含みます","normal":"現在入手可能なパートナーのみを含みます","event":"イベントでのみ入手可能なパートナーのみを含みます"} # 常駐絞り込み
types = {"B":"バランス","S":"サポート","C":"チャレンジ","?":"???"} # types
skills = {"-":"-","E":"Easy","H":"Hard","V":"Visual","M":"ミラー","O":"オーバーフロー","C":"チュウニズム","A":"Audio"} # skills

# ...settings end

# change_precence
@tasks.loop(minutes=1)
async def loop():
  global pindex
  if pindex == 0: v = f"Get help by typing 'a-help'"
  elif pindex == 1: v = f"Current ping is {round(bot.latency * 1000)}ms"
  elif pindex == 2: v = f"Let's play Arcaea!!!"
  elif pindex == 3: v = f"a-helpでヘルプを表示します"
  elif pindex == 4: v = f"現在のpingは{round(bot.latency * 1000)}msです"
  elif pindex == 5: v = f"さあ、Arcaeaをプレイしましょう！"
  await bot.change_presence(activity=dc.Game(name=v))
  pindex += 1 if pindex != 5 else -5
  
@bot.command()
async def help(ctx):
  await ctx.message.delete()
  e = dc.Embed(title="prefixは `a@` です",color=0x74596d)
  e.timestamp = dt.utcnow()
  e.add_field(name="help",value="ヘルプを表示します",inline=False)
  e.add_field(name="sinfo <曲名>",value="曲の情報を表示します",inline=False)
  e.add_field(name="pinfo <パートナー名>",value="パートナーの情報を表示します",inline=False)
  e.add_field(name="sselect (回数)",value="BOTがランダムに選曲します",inline=False)
  e.add_field(name="pselect",value="BOTがランダムにパートナーを選びます",inline=False)
  e.add_field(name="set",value="設定パネルを表示します",inline=False)
  e.add_field(name="Other",value="BOTの導入は[こちら](https://discord.com/api/oauth2/authorize?client_id=702587324718120991&permissions=60480&scope=bot)",inline=False)
  e.set_author(name="ヘルプ",icon_url=bot.user.avatar_url)
  e.set_footer(text=f"送信者 : {ctx.author.name}")
  await ctx.send(embed=e,delete_after=60)
  
@bot.command()
async def sinfo(ctx, *, name=None):
  await ctx.message.delete()
  if name == None:
    if dataset[0] != None: name = dataset[0]
    else: await ctx.send(embed=dc.Embed(title="曲名を入力して下さい"),delete_after=5.0)
  sgs = [i for i in sdata if name in i.name]
  if len(sgs) == 0: return await ctx.send(embed=dc.Embed(title="曲が見つかりませんでした"), delete_after=5.0)
  else: song = sgs[0]
  e = dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x00f1ff) if song.side == "光" else dc.Embed(title=f"◆ 曲名 {song.name}",description=f"◇ パック {song.pack}",color=0x461399)
  e.timestamp = dt.utcnow()
  e.add_field(name="◇ BPM",value=f"{song.bpm}",inline=False)
  e.add_field(name="◇ 作曲者 ・ アートワーク画像作者",value=f"{song.composer} ・ {song.illustrator}",inline=False)
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
    b.add_field(name="❖ 作曲者 ・ アートワーク画像作者",value=f"{song.composer} ・ {song.illustrator}",inline=False)
    b.add_field(name="❖ 難易度とノーツ数、譜面定数(BYD)",value=f"`譜面製作者`: {song.chart.BEYOND}\n`レベル`: {song.level.BEYOND}, `譜面定数`: {song.constant.BEYOND}\n`ノーツ数`: {song.notes.BEYOND}, `1ノート最高点`: {round(10000000 / int(song.notes.BEYOND), 3)}",inline=False)
    b.set_author(name="◆ 曲の情報(BYD) ❖",icon_url=bot.user.avatar_url)
    b.set_footer(text=f"送信者 : {ctx.author.name}")
    b.set_image(url=song.artwork.beyond)
    emojis, embeds, page = ["➡️","⬅️"], [e,b], 0
    m = await ctx.send(embed=embeds[0])
    while not bot.is_closed():
      await m.edit(embed=embeds[page])
      await m.add_reaction(emojis[page])
      try:
        r = await bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author and str(r.emoji) in emojis)
        await m.clear_reactions()
        if str(r[0]) == "➡️": page = 1
        else: page = 0
      except ao.TimeoutError:
        await m.delete()
        break
  else:
    await ctx.send(embed=e,delete_after=60)
  
@bot.command()
async def pinfo(ctx, *, name=None):
  await ctx.message.delete()
  if name == None:
    name = dataset[1] if dataset[1] != None else None
  partners = [i for i in pdata if name in i.name]
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
  enables_p = [i for i in sdata if not i.pack in sopt["ignorepacks"]] if len(sopt["ignorepacks"]) != 0 else sdata
  enables_so = [i for i in enables_p if not i in sopt["ignoresongs"]] if len(sopt["ignoresongs"]) != 0 else enables_p
  enables_si = [i for i in enables_so if i.side == sopt["side"]] if sopt["side"] != None else enables_so
  for song in enables_si:
    if song.level.BEYOND != "-":
      for level in sopt["levels"]:
        enables_si = [i for i in enables_si if [i.level.PAST,i.level.PRESENT,i.level.FUTURE,i.level.BEYOND][sopt["levels"].index(level)] in level] if len(level) != 0 else enables_si
    else:
      for level in sopt["levels"][0:3]:
        enables_si = [i for i in enables_si if [i.level.PAST,i.level.PRESENT,i.level.FUTURE][sopt["levels"].index(level)] in level] if len(level) != 0 else enables_si
  for nl in sopt["notes_limit"]:
    enables_si = [i for i in enables_si if nl[0] <= int([i.notes.PAST,i.notes.PRESENT,i.notes.FUTURE,i.notes.BEYOND][sopt["notes_limit"].index(nl)]) <= nl[1]]
  for cl in sopt["constant_limit"]:
    enables_si = [i for i in enables_si if cl[0] <= float([i.constant.PAST,i.constant.PRESENT,i.constant.FUTURE,i.constant.BEYOND][sopt["constant_limit"].index(cl)]) <= cl[1]]
  enables_co, enables_il, enables_ch = [], [], []
  if len(sopt["composers"]) != 0:
    for song in enables_si:
      for co in song.tags.composer:
        if co in sopt["composers"]:
          enables_co.append(song)
          pass
  else: enables_co = enables_si
  if len(sopt["illustrators"]) != 0:
    for song in enables_co:
      for il in song.tags.illustrator:
        if il in sopt["illustrators"]:
          enables_il.append(song)
          pass
  else: enables_il = enables_co
  if len(sopt["chart_creators"]) != 0:
    for song in enables_il:
      for ch in song.tags.chartdesigner:
        if ch in sopt["chart_creators"]:
          enables_ch.append(song)
          pass
  else: enables_ch = enables_il
  if len(enables_ch) == 0: return await ctx.send("条件に該当する楽曲が見つかりませんでした", delete_after=5.0)
  results = random.sample(enables_ch, count)
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
async def pselect(ctx, count=1):
  await ctx.message.delete()
  enables_r = [i for i in pdata if i.resident == popt["resident"]] if popt["resident"] != "all" else pdata
  enables_t = [i for i in enables_r if i.type in popt["types"]] if len(popt["types"]) != 0 else enables_r
  enables_s = [i for i in enables_t if i.skill.name in popt["skills"]] if len(popt["skills"]) != 0 else enables_t
  for fl in popt["frag_limit"]:
    enables_s = [i for i in enables_s if fl[0] <= float([i.frag.min,i.frag.max][popt["frag_limit"].index(fl)]) <= fl[1]]
  if len(enables_s) == 0: return await ctx.send("条件に該当するパートナーが見つかりませんでした", delete_after=5.0)
  result = random.sample(enables_s, count)
  for partner in result:
    e = dc.Embed(title=f"◆ パートナー名 {partner.name}",description=f"◇ タイプ {partner.type}",color=0x74596d)
    e.timestamp = dt.utcnow()
    e.set_author(name="❖ パートナー選択 ❖",icon_url=bot.user.avatar_url)
    e.set_footer(text=f"詳細は a.partner_info で確認できます\n送信者 : {ctx.author.name}")
    await ctx.send(embed=e)
    dataset[1] = partner.name 
  
@bot.command(name="set")
async def setting(ctx):
  await ctx.message.delete()
  start_e = dc.Embed(title="1】どうしますか？",description="**`end`** : 設定 終了\n**`check`** : 設定 確認\n**`song`** : 条件設定 (楽曲自動選択)\n**`partner`** : 条件設定 (パートナー自動選択)",color=0x005AD6)
  ssstart_e = dc.Embed(title="2=S】設定項目を選択して下さい",description="**`ip`** : 除外/追加 (パック)\n**`is`** : 除外/追加 (楽曲)\n**`l`** : 対象設定 (レベル)\n**`s`** : 対象設定 (サイド)\n**`nl`** : 上下限設定 (ノーツ数)\n**`cl`** : 上下限設定 (譜面定数)\n**`co`** : 対象設定 (作曲者)\n**`il`** : 対象設定 (イラストレーター)\n**`ch`** : 対象設定 (譜面製作者)",color=0x6FFFBA)
  ignorepack_e = dc.Embed(title="3=S-ip】以下から選択して下さい\n(以下短縮名称を使用してください)",description="`Ae`(Archive)  `Aa`(Arcaea)\n`WE`(World Extend) `BF`(Black Fate)\n`AP`(Adverse Prelude)\n`LS`(Luminous Sky) `VL`(Vicious Labyrinth)\n`EC`(Eternal Core) `SR`(Sunset Radiance)\n`AR`(Absolute Reason) `BE`(Binary Enfold)\n`Am`(Ambivalent Vision)\n`CS`(Crimson Solace) `CH`(CHUNITHM)\n`GC`(Groove Coaster) `TS`(Tone Sphere)\n`La`(Lanota) `Dx`(Dynamix)",color=0x6FFFBA)
  ignoresong_e = dc.Embed(title="3=S-is】楽曲名を入力して下さい\n※曲名は完全一致である必要はありません\n(類似する楽曲がある場合を除く)",color=0x6FFFBA)
  level_e = dc.Embed(title="3=S-l】以下から選択して下さい",description="`pst` : PAST基準\n`prs` : PRESENT基準\n`ftr` : FUTURE基準\n`byd` : BEYOND基準",color=0x6FFFBA)
  lpst_e = dc.Embed(title="4=S-l-pst】数値を入力して下さい\n(`下限` : 1 , `上限` : 6)")
  lprs_e = dc.Embed(title="4=S-l-prs】数値を入力して下さい\n(`下限` : 3 , `上限` : 9)")
  lftr_e = dc.Embed(title="4=S-l-ftr】数値を入力して下さい\n(`下限` : 7 , `上限` : 11)")
  lbyd_e = dc.Embed(title="4=S-l-byd】数値を入力して下さい\n(`下限` : 8 , `上限` : 11)")
  side_e = dc.Embed(title="3=S-s】以下から選択して下さい",description="`all` : 全てを含みます\n`light` : サイドを光のみにします\n`conflict` : サイドを対立のみにします",color=0x6FFFBA)
  noteslimit_e = dc.Embed(title="3=S-nl】以下から選択して下さい",description="`pst` : PAST基準\n`prs` : PRESENT基準\n`ftr` : FUTURE基準\n`byd` : BEYOND基準",color=0x6FFFBA)
  nlpst_e = dc.Embed(title="4=S-nl-pst】数値を2つ入力してください\n2つの数値は整数にして下さい\n2つの数値の間には半角空白を入れて下さい",color=0x0EA3FF )
  nlprs_e = dc.Embed(title="4=S-nl-prs】数値を2つ入力してください\n2つの数値は整数にして下さい\n2つの数値の間には半角空白を入れて下さい",color=0x0ACD38 )
  nlftr_e = dc.Embed(title="4=S-nl-ftr】数値を2つ入力してください\n2つの数値は整数にして下さい\n2つの数値の間には半角空白を入れて下さい",color=0xDB3DBC )
  nlbyd_e = dc.Embed(title="4=S-nl-byd】数値を2つ入力してください\n2つの数値は整数にして下さい\n2つの数値の間には半角空白を入れて下さい",color=0xFF0000 )
  constantlimit_e = dc.Embed(title="3=S-cl】以下から選択して下さい",description="`pst` : PAST基準\n`prs` : PRESENT基準\n`ftr` : FUTURE基準\n`byd` : BEYOND基準",color=0x6FFFBA)
  clpst_e = dc.Embed(title="4=S-cl-pst】数値を2つ入力してください\n2つの数値は整数でなくとも構いません\n2つの数値の間には半角空白を入れて下さい",color=0x0EA3FF)
  clprs_e = dc.Embed(title="4=S-cl-prs】数値を2つ入力してください\n2つの数値は整数でなくとも構いません\n2つの数値の間には半角空白を入れて下さい",color=0x0ACD38)
  clftr_e = dc.Embed(title="4=S-cl-ftr】数値を2つ入力してください\n2つの数値は整数でなくとも構いません\n2つの数値の間には半角空白を入れて下さい",color=0xDB3DBC)
  clbyd_e = dc.Embed(title="4=S-cl-byd】数値を2つ入力してください\n2つの数値は整数でなくとも構いません\n2つの数値の間には半角空白を入れて下さい",color=0xFF0000)
  composer_e = dc.Embed(title="3=S-co】作曲者名を入力して下さい\n※作曲者名は完全一致でなくとも問題ありません\n(類似する場合を除く)",description="- 作曲者名一覧\n(1部名義は集約してあります)\n```T2Kazuya, chitose, a-zu-ra, 南ゆに(アリスシャッハと魔法の楽団), Sound Souler , U-ske, lueur, Tiny Minim, Frums, HyuN, 旅人E, REDSHiFT, Blacklolita, しーけー, Arch, n3pu, ARForest, Iris, gmtn., Missionary, DIA, Aire, ak+q, WHITEFISTS, Sakuzyo, Jun Kuroda, Farhan, Kolaa, Puru, THB, Sta(THE SHAFT), sky_delta, お月さま交響曲, Rabbit House, Ryazan, Combatplayer, Soleily, Yooh, void, cYsmix, wa., DJ Myosuke(HARDCORE TANO\*C), 7mai, 3R2, Cosmograph, Mameyudoufu, uno, ちょこ, Silentroom, アリスシャッハと魔法の楽団, REDALiCE(HARDCORE TANO*C), siromaru(INNOCENT NOISE), t+pazolite(HARDCORE TANO\*C), TQ☆, ikaruga_nex, Feryquitous, Sennzai, MYTK, Ras, BACO, 溝口ゆうま, 大瀬良あい, WHITEFIST, からとpαnchii少年, はるの, MYUKKE., ginkiha, Sampling Masters MEGA, TANO*C Sound Team, USAO(HARDCORE TANO\*C), DJ Genki(HARDCORE TANO*C), DJ Noriken(HARDCORE TANO\*C), P*Light(HARDCORE TANO\*C), 黒皇帝, Laur, Street, Maozon, Noah, 光吉猛修, Zekk, Apo11o program, ETIA., HiTECH NINJA, Saiph, Virtual Self, HATE, Junk, Mitomoro, Mili, PSYQUI, Nitro, Missive New Krew, かゆき, Syepias, jioyi, Tanchiky, xi, nora2r, Gram, YUKIYANAGI, Nhato, EBIMAYO, Yamajet, Powerless, Aoi, siqlo, モリモリあつし, Yunosuke, MASAKI, ぺのれり, Kobaryo, WAiKURO, Cranky, cybermiso, 翡乃イスカ, uma, LeaF, Polysha, 橘花音, Akira Complex, Juggernaut., A.SAKA, Team Grimoire, かめりあ(EDP), Edelritter```",color=0x6FFFBA)
  illustrator_e = dc.Embed(title="3-S-il】名前を入力して下さい\n※名前は完全一致である必要はありません\n(類似する場合を除く)",description="- イラストレーター名一覧\n```T2Kazuya, Khronetic, 不明, 白鳥怜, ましろみ のあ, 橙乃遥, Hanamori Hiro, Tagtraume, NanoKun, 黒刃愛, grosspanda, 釜飯轟々丸, かぐやのもちづき, yoshimo, Shionty, RiceGnat, Ancy, 雨風雪夏, Mechari, terry, nakanome, レアル, Saga, キッカイキ, mins, Frums, VMWT, シエラ, deronoitz, Megu, お月さま交響曲, YEONIE, 織日ちひろ, Doomfest, CinEraLiA, 八葉, Koyama Mai, Eric Dagley, 百舌谷, トロ3, Refla, BerryVerrine, Photonskyto, DJ Poyoshi, unKn, アリスシャッハと魔法の楽団, nonokuro, 駿, HenryTz, 出前, 魔界の住人, 未早, softmode, kobuta, ふぇいフリック, SiNoe, LAM, Sta, NTFS, 巻羊, mokeo, fixro2n, rtil, 和音ハカ, wacca, hideo, yusi., クルエルGZ, スズカミ, そゐち, 久賀フーナ, Hie, mirimo, iimo, すずなし, きらばがに, Sou, SKT, アサヤ, 吠L, EB十, 姐川, リウイチ, 岩十, horte, deel, GreeN, SERXPHIS, Rolua, NAGU, 望月けい, KEI```",color=0x6FFFBA)
  chart_creator_e = dc.Embed(title="3-S-ch】譜面製作者名を入力して下さい\n※製作者名は完全一致でなくとも問題ありません\n(類似する場合を除く)",description="- 譜面製作者名一覧\n(1部名義は集約してあります)\n```Nitro(夜浪などを含む), Toaster(東星などを含む), Kurorak(黒運などを含む), k//eternal(chaos//engineなどを含む), -chartaesthesia-, TaroNuke, 石樂, Exschwation, Black Tea, Arcaea Team, 緑, CERiNG, Kero, Darkest Dream, 不明, /(Arcahv), Arcaea Charting Team, The Monolith, Zero Sky, Paradox(Fracture Ray), 迷路(Grievous Lady), Tempest(Tempestissimo)```",color=0x6FFFBA)
  psstart_e = dc.Embed(title="2=P】設定項目を選択して下さい",description="**`r`** : 除外/追加 (恒常・期間限定)\n**`t`** : 対象設定 (タイプ)\n**`s`** : 対象設定 (スキル)\n**`fl`** : 上下限設定 (FRAG)\n**`sl`** : 上下限設定 (Step)",color=0xFFD200)
  resident_e = dc.Embed(title="3=P-r】以下から選択して下さい",description="`all` : 全て含みます\n`normal` : 恒常パートナーのみ\n`event` : 期間限定パートナーのみ",color=0xFFD200)
  type_e = dc.Embed(title="3=P-t】以下から選択して下さい\n(以下短縮名称を使用して下さい)",description="**`B`** (バランス)\n**`S`** (サポート)\n**`C`** (チャレンジ)\n**`?`** (???)",color=0xFFD200)
  skill_e = dc.Embed(title="3=P-s】以下から選択して下さい\n(以下短縮名称を使用して下さい)",description="**`-`** (-)\n**`E`** (Easy)\n**`H`** (Hard)\n**`V`** (Visual)\n**`M`** (ミラー)\n**`O`** (オーバーフロー)\n**`C`** (チュウニズム)\n**`A`** (Audio)",color=0xFFD200)
  flaglimit_e = dc.Embed(title="3=P-fl】以下から選択して下さい",description="`initial` : Lv1 基準\n`highest` : Lv20 基準",color=0xFFD200)
  flinitial_e = dc.Embed(title="4=P-fl-il】数値を2つ入力して下さい\n・2つの数値は整数でなくとも構いません\n・数値の間には半角空白を入れて下さい",color=0xFFC77E)
  flhighest_e = dc.Embed(title="4=P-fl-ht】数値を2つ入力して下さい\n・2つの数値は整数でなくとも構いません\n・数値の間には半角空白を入れて下さい",color=0x758500)                      
  steplimit_e = dc.Embed(title="3=P-sl】以下から選択して下さい",description="`initial` : Lv1 基準\n`highest` : Lv20 基準",color=0xFFD200)
  slinitial_e = dc.Embed(title="4=P-sl-il】数値を2つ入力して下さい\n・2つの数値は整数でなくとも構いません\n・数値の間には半角空白を入れて下さい",color=0xFFC77E)
  slhighest_e = dc.Embed(title="4=P-sl-ht】数値を2つ入力して下さい\n・2つの数値は整数でなくとも構いません\n・数値の間には半角空白を入れて下さい",color=0x758500)                      
  
  page = 0
  embeds = {
    0: start_e,
    1: ssstart_e,
    2: ignorepack_e,
    3: ignoresong_e,
    4: level_e,
    5: lpst_e,
    6: lprs_e,
    7: lftr_e,
    8: lbyd_e,
    9: side_e,
    10: noteslimit_e,
    11: nlpst_e,
    12: nlprs_e,
    13: nlftr_e,
    14: nlbyd_e,
    15: constantlimit_e,
    16: clpst_e,
    17: clprs_e,
    18: clftr_e,
    19: clbyd_e,
    20: composer_e,
    21: illustrator_e,
    22: chart_creator_e,
    23: psstart_e,
    24: resident_e,
    25: type_e,
    26: skill_e,
    27: flaglimit_e,
    28: flinitial_e,
    29: flhighest_e,
    30: steplimit_e,
    31: slinitial_e,
    32: slhighest_e
  }
                        
  emb = await ctx.send(embed=embeds[0])
  while not bot.is_closed():
    await emb.edit(embed=embeds[page])
    try:
      msg = await bot.wait_for('message', timeout=120.0, check=lambda m: m.author == ctx.author)
      await msg.edit(delete_after=2.0)
      if page == 0:
        if msg.content == "end":
          await emb.delete()
          break
        elif msg.content == "check":
          ip_display = '\n'.join(sopt["ignorepacks"]) if len(sopt["ignorepacks"]) != 0 else "なし"
          is_display = '\n'.join(list(map(lambda x: x.name, sopt["ignoresongs"]))) if len(sopt["ignoresongs"]) != 0 else "なし"
          l_display_pst = ' '.join(sopt["levels"][0]) if len(sopt["levels"][0]) != 0 else "なし"
          l_display_prs = ' '.join(sopt["levels"][1]) if len(sopt["levels"][1]) != 0 else "なし"         
          l_display_ftr = ' '.join(sopt["levels"][2]) if len(sopt["levels"][2]) != 0 else "なし"
          l_display_byd = ' '.join(sopt["levels"][3]) if len(sopt["levels"][3]) != 0 else "なし"
          co_display = '\n'.join(sopt["composers"]) if len(sopt["composers"]) != 0 else "全て"
          il_display = '\n'.join(sopt["illustrators"]) if len(sopt["illustrators"]) != 0 else "全て"
          ch_display = '\n'.join(sopt["chart_creators"]) if len(sopt["chart_creators"]) != 0 else "全て"
          t_display = ' '.join(popt["types"]) if len(popt["types"]) != 0 else "全て"
          s_display = ' '.join(popt["skills"]) if len(popt["skills"]) != 0 else "全て"
          ignores_e = dc.Embed(title="◇ 自動選択設定 - 楽曲(1/4)",color=0x74596d)
          ignores_e.add_field(name="❖ 除外パック",value=ip_display,inline=False)
          ignores_e.add_field(name="❖ 除外楽曲",value=is_display,inline=False)
          levels_e = dc.Embed(title="◇ 自動選択設定 - 楽曲(2/4)",description="❖ レベル制限",color=0x74596d)
          levels_e.add_field(name="**PAST基準 -**",value=l_display_pst,inline=False)
          levels_e.add_field(name="**PRESENT基準 -**",value=l_display_prs,inline=False)
          levels_e.add_field(name="**FUTURE基準 -**",value=l_display_ftr,inline=False)
          levels_e.add_field(name="**BEYOND基準 -**",value=l_display_byd,inline=False)
          infos_e = dc.Embed(title="◇ 自動選択設定 - 楽曲(4/4)",color=0x74596d)
          infos_e.add_field(name="❖ サイド",value=sopt['side'],inline=False)
          infos_e.add_field(name="❖ 作曲者",value=co_display,inline=False)
          infos_e.add_field(name="❖ イラストレーター",value=il_display,inline=False)
          infos_e.add_field(name="❖ 譜面製作者",value=ch_display,inline=False)
          jopt = [
            [
              ' 〜 '.join([str(x) for x in sopt["notes_limit"][0]]),
              ' 〜 '.join([str(x) for x in sopt["notes_limit"][1]]),
              ' 〜 '.join([str(x) for x in sopt["notes_limit"][2]]),
              ' 〜 '.join([str(x) for x in sopt["notes_limit"][3]])
            ],
            [
              ' 〜 '.join([str(x) for x in sopt["constant_limit"][0]]),
              ' 〜 '.join([str(x) for x in sopt["constant_limit"][1]]),
              ' 〜 '.join([str(x) for x in sopt["constant_limit"][2]]),
              ' 〜 '.join([str(x) for x in sopt["constant_limit"][3]])
            ],
            [
              ' 〜 '.join([str(x) for x in popt["frag_limit"][0]]),
              ' 〜 '.join([str(x) for x in popt["frag_limit"][1]])
            ],
            [
              ' 〜 '.join([str(x) for x in popt["step_limit"][0]]),
              ' 〜 '.join([str(x) for x in popt["step_limit"][1]])
            ]
          ]
          limits_e = dc.Embed(title="◇ 自動選択設定 - 楽曲(3/4)",description="❖ 制限",color=0x74596d)
          limits_e.add_field(name="**PAST基準**",value=f"`ノーツ数` : {jopt[0][0]}\n`譜面定数` : {jopt[1][0]}",inline=False)
          limits_e.add_field(name="**PRESENT基準**",value=f"`ノーツ数` : {jopt[0][1]}\n`譜面定数` : {jopt[1][1]}",inline=False)
          limits_e.add_field(name="**FUTURE基準**",value=f"`ノーツ数` : {jopt[0][2]}\n`譜面定数` : {jopt[1][2]}",inline=False)
          limits_e.add_field(name="**BEYOND基準**",value=f"`ノーツ数` : {jopt[0][3]}\n`譜面定数` : {jopt[1][3]}",inline=False)
          partner_e = dc.Embed(title="◇ 自動選択設定 - パートナー",color=0x74596d)
          partner_e.add_field(name="❖ 対象",value=display_resident[popt['resident']],inline=False)
          partner_e.add_field(name="❖ タイプ制限",value=t_display,inline=False)
          partner_e.add_field(name="❖ レベル制限",value=s_display,inline=False)
          partner_e.add_field(name="❖ FRAG制限",value=f"**Lv1基準** : {jopt[2][0]}\n**Lv20基準** : {jopt[2][1]}",inline=False)
          partner_e.add_field(name="❖ STEP制限",value=f"**Lv1基準** : {jopt[3][0]}\n**Lv20基準** : {jopt[3][1]}",inline=False)
          check_embeds = [ignores_e,levels_e,limits_e,infos_e,partner_e] 
          check_page = 0
          while not bot.is_closed():
            await emb.edit(embed=check_embeds[check_page])
            await emb.add_reaction("❌")
            if check_page == 0: await emb.add_reaction("➡️")
            elif check_page == 4: await emb.add_reaction("⬅️")
            else:
              await emb.add_reaction("⬅️")
              await emb.add_reaction("➡️")
            react = await bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and str(r.emoji) in ["❌","➡️","⬅️"])
            await emb.clear_reactions()
            if str(react[0]) == "➡️": check_page += 1
            elif str(react[0]) == "⬅️": check_page -= 1
            else: 
              page = 0
              break
        elif msg.content == "song": page = 1
        elif msg.content == "partner": page = 23
        else:
          pass
      else:
        if msg.content == "back": 
          if page in [1,23]:
            page = 0
          elif page not in [5,6,7,8,11,12,13,14,16,17,18,19,28,29,31,32]:
            if 2 <= page <= 22: page = 1
            elif 24 <= page <= 32: page = 23
          else:
            if 5 <= page <= 8: page = 4
            elif 11 <= page <= 14: page = 10
            elif 16 <= page <= 19: page = 15
            elif 28 <= page <= 29: page = 27
            else: page = 30
        elif page == 1: # song_start
          if msg.content in sfirst:
            page = sfirst[msg.content]
          else:
            pass
        elif page == 2: # song_ignore_pack
          if msg.content in ignorepacks:
            if ignorepacks[msg.content] in sopt["ignorepacks"]:
              del sopt["ignorepacks"][sopt["ignorepacks"].index(ignorepacks[msg.content])]
            else:
              sopt["ignorepacks"].append(ignorepacks[msg.content])
            page = 1 
          else:
            pass
        elif page == 3: # song_ignore_songs
          for s in sdata:
            if msg.content in s.name:
              if s in sopt["ignoresongs"]:
                del sopt["ignoresongs"][sopt["ignoresongs"].index(s)]
              else:
                sopt["ignoresongs"].append(s)
              page = 1
        elif page in [4,10,15]: # difficulty_select
          if msg.content in ["pst","prs","ftr","byd"]:
            page += {"pst":1,"prs":2,"ftr":3,"byd":4}[msg.content]
          else:
            pass
        elif 5 <= page <= 8: # level
          if msg.content in {5:["1","2","3","4","5","6"],6:["3","4","5","6","7","8","9"],7:["7","8","9","9+","10","10+","11"],8:["8","9","9+","10","10+","11"]}[page]:
            if msg.content in sopt["levels"][{5:0,6:1,7:2,8:3}[page]]:
              del sopt["levels"][{5:0,6:1,7:2,8:3}[page]][sopt["levels"][{5:0,6:1,7:2,8:3}[page]].index(msg.content)]
            else:
              sopt["levels"][{5:0,6:1,7:2,8:3}[page]].append(msg.content)
            page = 1
          else:
            pass
        elif 11 <= page <= 14:
          splits = msg.content.split(" ")
          try:
            nlvalues = [int(x) for x in splits]
          except Exception:
            pass
          else:
            sopt["notes_limit"][{11:0,12:1,13:2,14:3}[page]][0] = nlvalues[0]
            sopt["notes_limit"][{11:0,12:1,13:2,14:3}[page]][1] = nlvalues[1]
            page = 1
        elif page == 9:
          if msg.content in sides:
            sopt["side"] = sides[msg.content]
            page = 1
          else:
            pass
        elif 20 <= page <= 22:
          values = list(filter(lambda x:msg.content in x, {20:composers,21:illustrators,22:chart_creators}[page]))
          if len(values) != 0:
            if values[0] in sopt[{20:"composers",21:"illustrators",22:"chart_creators"}[page]]:
              del sopt[{20:"composers",21:"illustrators",22:"chart_creators"}[page]][sopt[{20:"composers",21:"illustrators",22:"chart_creators"}[page].index(values[0])]]
            else:
              sopt[{20:"composers",21:"illustrators",22:"chart_creators"}[page]].append(values[0])
            page = 1
          else: 
            pass
        elif page == 23: # partner_start
          if msg.content in pfirst:
            page = pfirst[msg.content]
          else:
            pass                
        elif page == 24: # resident
          if msg.content in ["all","normal","event"]:
            popt["resident"] = msg.content
            page = 23
          else:
            pass
        elif page == 25: # type
          if msg.content in types:
            if types[msg.content] in popt["types"]:
              del popt["types"][popt["types"].index(types[msg.content])]
            else:
              popt["types"].append(types[msg.content])
            page = 23
          else:
            pass
        elif page == 26: # skill
          if msg.content in skills:
            if skills[msg.content] in popt["skills"]:
              del popt["skills"][popt["skills"].index(skills[msg.content])]
            else:
              popt["skills"].append(skills[msg.content])
            page = 23
          else:
            pass
        elif page in [27,30]:
          if msg.content == "initial":
            page += 1
          elif msg.content == "highest":
            page += 2
          else:
            pass
        elif page in [16,17,18,19,28,29,31,32]:
          splits = msg.content.split(" ")
          try:
            clvalues = [float(x) for x in splits]
          except Exception:
            pass
          else:
            if 16 <= page <= 19:
              sopt["constant_limit"][{16:0,17:1,18:2,19:3}[page]][0] = clvalues[0]
              sopt["constant_limit"][{16:0,17:1,18:2,19:3}[page]][1] = clvalues[1]
            elif 28 <= page <= 32:
              popt[{28:"frag_limit",29:"frag_limit",31:"step_limit",32:"step_limit"}[page]][{28:0,29:1,31:0,32:1}[page]][0] = clvalues[0]
              popt[{28:"frag_limit",29:"frag_limit",31:"step_limit",32:"step_limit"}[page]][{28:0,29:1,31:0,32:1}[page]][1] = clvalues[1]
            page = {16:1,17:1,18:1,19:1,28:23,29:23,31:23,32:23}[page]
          
    except ao.TimeoutError:
      await emb.delete()
      break
                        
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
