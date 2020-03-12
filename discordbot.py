# インストールした discord.py を読み込む 
import discord

#その他もimport
from discord.utils import get
from discord.ext import tasks
from datetime import datetime
import random
import json
import asyncio
import sys
import urllib.request 
import re
import datetime

citycodes = { 
  "稚内" : "011000", "旭川" : "012010",
  "留萌" : "012020", "札幌" : "016010",
  "岩見沢" : "016020", "倶知安" : "016030",
  "網走" : "013010", "北見" : "013020",
  "紋別" : "013030", "根室" : "014010",
  "釧路" : "014020", "帯広" : "014030",
  "室蘭" : "015010", "浦河" : "015020",
  "函館" : "017010", "江差" : "017020",
  "青森" : "020010", "むつ" : "020020",
  "八戸" : "020030", "盛岡" : "030010",
  "宮古" : "030020", "大船渡" : "030030",
  "仙台" : "040010", "白石" : "040020",
  "秋田" : "050010", "横手" : "050020",
  "山形" : "060010", "米沢" : "060020",
  "酒田" : "060030", "新庄" : "060040",
  "福島" : "070010", "小名浜" : "070020",
  "若松" : "070030", "東京" : "130010",
  "大島" : "130020", "八丈島" : "130030",
  "父島" : "130040", "横浜" : "140010",
  "小田原" : "140020", "さいたま" : "110010",
  "熊谷" : "110020", "秩父" : "110030",
  "千葉" : "120010", "銚子" : "120020",
  "館山" : "120030", "水戸" : "080010",
  "土浦" : "080020", "宇都宮" : "090010",
  "大田原" : "090020", "前橋" : "100010",
  "みなかみ" : "100020", "甲府" : "190010",
  "河口湖" : "190020", "新潟" : "150010",
  "長岡" : "150020", "高田" : "150030",
  "相川" : "150040", "長野" : "200010",
  "松本" : "200020", "飯田" : "200030",
  "富山" : "160010", "伏木" : "160020",
  "金沢" : "170010", "輪島" : "170020",
  "福井" : "180010", "敦賀" : "180020",
  "名古屋" : "230010", "豊橋" : "230020",
  "岐阜" : "210010", "高山" : "210020",
  "静岡" : "220010", "網代" : "220020",
  "三島" : "220030", "浜松" : "220040",
  "津" : "240010", "尾鷲" : "240020",
  "大阪" : "270000", "神戸" : "280010",
  "豊岡" : "280020", "京都" : "260010",
  "舞鶴" : "260020", "大津" : "250010",
  "彦根" : "250020", "奈良" : "290010",
  "風屋" : "290020", "和歌山" : "300010",
  "潮岬" : "300020", "鳥取" : "310010",
  "米子" : "310020", "松江" : "320010",
  "浜田" : "320020", "西郷" : "320030",
  "岡山" : "330010", "津山" : "330020",
  "広島" : "340010", "庄原" : "340020",
  "下関" : "350010", "山口" : "350020",
  "柳井" : "350030", "荻" : "350040",
  "徳島" : "360010", "日和佐" : "360020",
  "高松" : "370000", "松山" : "380010",
  "新居浜" : "380020", "宇和島" : "380030",
  "高知" : "390010", "室戸岬" : "390020",
  "清水" : "390030", "福岡" : "400010",
  "八幡" : "400020", "飯塚" : "400030",
  "久留米" : "400040", "大分" : "440010",
  "中津" : "440020", "日田" : "440030",
  "佐伯" : "440040", "長崎" : "420010",
  "佐世保" : "420020", "厳原" : "420030",
  "福江" : "420040", "佐賀" : "410010",
  "伊万里" : "410020", "熊本" : "430010",
  "阿蘇乙姫" : "430020", "牛深" : "430030",
  "人吉" : "430040", "宮崎" : "450010",
  "延岡" : "450020", "都城" : "450030",
  "高千穂" : "450040", "鹿児島" : "460010",
  "鹿屋" : "460020", "種子島" : "460030",
  "名瀬" : "460040", "那覇" : "471010",
  "名護" : "471020", "久米島" : "471030",
  "南大東" : "472000", "宮古島" : "473000",
  "石垣島" : "474010", "与那国島" : "474020"
}

chihos = ["北海道地方", "東北地方", "関東地方", "中部地方", "近畿地方", "中国/四国地方", "九州地方"]

exceptn = [598355101845028895]

# Embed一覧 [client.1]
#embed,embed1,embed2,embed3,embed4,embed5,
#embed6,embed7,embed8,embed9,embed10,embed11
#embed12,embed13

# 自分のBotのアクセストークンに置き換えてください 
TOKEN = 'NjQyMzIwOTUxOTg3NTM1ODkz.XcllpA.boi648C-XGgEVXyzbICFVTX01hA' 

# 接続に必要なオブジェクトを生成
client = discord.Client()

@client.event 
async def on_member_join(member):
  gn1 = member.guild.name
  gn2 = datetime.datetime.now().strftime('%Y年%m月%日 %H時%M分')
  gn3 = member.avatar_url
  embed13 = discord.Embed(title="Join",description=str(gn2),color=0xabc9ec)
  embed13.add_field(name=str(member) + " さんが",value=str(gn1) + " に参加しました")
  embed13.set_thumbnail(url=gn3)
  ch_name = "cjoin-log"
  for channel in member.guild.channels: 
    if channel.name == ch_name:
      await channel.send(embed=embed13)
  #channel = client.get_channel(661142331403010078)
  #await channel.send(embed=embed8)
  
@client.event 
async def on_member_remove(member):
  gn4 = member.guild.name
  gn5 = datetime.datetime.now().strftime('%Y年%m月%日 %H時%M分')
  gn6 = member.avatar_url
  embed12 = discord.Embed(title='left',description=str(gn5),color=0xabc9ec)
  embed12.add_field(name=str(member) + " さんが",value=str(gn4) + " から退出しました")
  embed12.set_thumbnail(url=gn6)
  ch_name = "cleave-log" 
  for channel in member.guild.channels: 
    if channel.name == ch_name:
      await channel.send(embed=embed12)
  #channel = client.get_channel(661142435694510084)
  #await channel.send(embed=embed9)
  
# 起動時に動作する処理 
@client.event 
async def on_ready():  
  den = client.guilds
  den1 = len(den)
  date = datetime.datetime.now().strftime('%Y年%m月%d日 %H時%M分')
  print("------------------------------------")
  print("[" + date + "]" + 'ClariceBOT-start!')
  print("------------------------------------")
  
  embed11 = discord.Embed(title="ClariceBOT",description="LOGS",color=0xabc9ec)
  embed11.add_field(name="起動しました！",value="導入サーバー数 : " + str(den1))
  embed11.add_field(name="起動時刻",value=str(date))
  
  ch_name = "cb-log" 
  for channel in client.get_all_channels(): 
    if channel.name == ch_name:
      await channel.send(embed=embed11)
  await client.change_presence(activity=discord.Game(name='c!help | ClariceBOT')) 

 
# 45秒ループ
@tasks.loop(seconds=60)
async def loop():  
  now = datetime.datetime.now().strftime('%H:%M')
  if now == '00:00' or now == '03:00' or now == '06:00' or now == '09:00' or now == '12:00' or now == '15:00' or now == '18:00' or now == '21:00':
    if now == '00:00':
      lmsg = "| 午前 0 時 | latency check |"
    elif now == '03:00':
      lmsg = "| 午前 3 時 | latency check |"
    elif now == '06:00':
      lmsg = "| 午前 6 時 | latency check |"
    elif now == '09:00':
      lmsg = "| 午前 9 時 | latency check |"
    elif now == '12:00':
      lmsg = "| 午後 0 時 | latency check |"
    elif now == '15:00':
      lmsg = "| 午後 3 時 | latency check |"
    elif now == '18:00':
      lmsg = "| 午後 6 時 | latency check |"
    elif now == '21:00':
      lmsg = "| 午後 9 時 | latency check |"  
    laten = client.latency
    embed10 = discord.Embed(title="ClariceBOT",description="",color=0xabc9ec)
    embed10.add_field(name=lmsg,value=str(laten) + "秒")
    channel = client.get_channel(670200667717238824)
    await channel.send(embed=embed15)
    
@client.event
async def on_message(message):
 
  # exceptnに登録した輩は消し飛ばす
  if message.author.id in exceptn:
    return  
  
  # commands_log
  def command_log():
    with open("ClariceBOT_Commands_Log.json", "r", encoding="utf-8") as log:
      logs = json.load(log)
    log_time = datetime.datetime.now().strftime("%Y.%m.%d.%H:%M")
    log_name = message.author.name
    log_date = message.content
    logs.setdefault("[" + log_time + "/" + log_name + "]", "[" + log_date + "]")
    with open("ClariceBOT_Commands_Log.json", "w", encoding="utf-8") as log:
      json.dump(logs, log)
  
  # 停止 
  if message.content == "c!exit" or message.content == "c!e":
    if message.author.id == 536506865883021323 or message.author.id == 537031688610512896:
      await message.delete()
      date = datetime.datetime.now().strftime('%Y年%m月%d日 %H時%M分')
      gu_name = message.author.guild.name   
      await message.author.send('終了します')     
      embed9 = discord.Embed(title="ClariceBOT",description="LOGS",color=0xabc9ec)
      embed9.add_field(name="停止しました！",value="コマンド出力元 : " + gu_name)
      embed9.add_field(name="停止時刻",value=str(date))   
      ch_name = "cb-log" 
      for channel in client.get_all_channels(): 
        if channel.name == ch_name:
          await channel.send(embed=embed9)
      print("----------------------------------------")
      print('[' + str(date) + ']' + 'ClariceBOT-stop!')
      print("----------------------------------------")
      command_log()
      await client.logout() 
      await sys.exit()
    else:
      await message.delete()
      await message.channel.send('このコマンドを使用可能なのは開発者のみです')
  
  #天気を調べます
  if message.content.startswith('c!weather'):
    weamsgs = message.content.split()
    if len(weamsgs) == 1:
      embed8 = discord.Embed(title="Weather",description="ヘルプ")
      embed8.add_field(name="c!weather `地名`で調べられます",value="c!weather `地方名`で調べられる地名が分かります(以下参照)")
      embed8.add_field(name="| 地方名 一覧 |",value="・北海道地方\n・東北地方\n・関東地方\n・中部地方\n・近畿地方\n・中国/四国地方\n・九州地方")
      await message.channel.send(embed=embed8)
      command_log()
    elif len(weamsgs) == 2:          
      chiho = weamsgs[1]
      if chiho in chihos:
        embed11 = discord.Embed(title="Weather",description=chiho + " | 可能地名一  覧")
        if chiho == "北海道地方":
          embed11.add_field(name="-北海道-",value="・稚内\n・旭川\n・留萌\n・札幌\n・岩見沢\n・倶知安\n・網走\n・北見\n・紋別\n・根室\n・釧路\n・帯広\n・室蘭\n・浦河\n・函館\・江差")
        elif chiho == "東北地方":
          embed11.add_field(name="-青森県-",value="・青森\n・むつ\n・八戸")
          embed11.add_field(name="-岩手県-",value="・盛岡\n・宮古\n・  大船渡")
          embed11.add_field(name="-宮城県-",value="・仙台\n・白石")
          embed11.add_field(name="-秋田県-",value="・秋田\n・横手")
          embed11.add_field(name="-山形県-",value="・山形\n・米沢\n・酒田\n・新庄")
          embed11.add_field(name="-福島県-",value="・福島\n・小名浜\n・若松")
        elif chiho == "関東地方":
          embed11.add_field(name="-東京都-",value="・東京\n・大島\n・八丈島\n・父島")
          embed11.add_field(name="-神奈川県-",value="・横浜\n・小田原")
          embed11.add_field(name="-埼玉県-",value="・さいたま\n・熊谷\n・秩父")
          embed11.add_field(name="-千葉県-",value="・千葉\n・銚子\n・館山")
          embed11.add_field(name="-茨城県-",value="・水戸\n・土浦")
          embed11.add_field(name="-栃木県-",value="・宇都宮\n・大田原")
          embed11.add_field(name="-群馬県-",value="・前橋\n・ みなかみ")
        elif chiho == "中部地方":
          embed11.add_field(name="-山梨県-",value="・甲府\n・河口湖")
          embed11.add_field(name="-新潟県-",value="・新潟\n・長岡\n・高田\n・相川")
          embed11.add_field(name="-長野県-",value="・長野\n・松本\n・飯田")
          embed11.add_field(name="-富山県-",value="・富山\n・伏木")
          embed11.add_field(name="-石川県-",value="・金沢\n・輪島")
          embed11.add_field(name="-福井県-",value="・福島\n・敦賀")
          embed11.add_field(name="-愛知県-",value="・名古屋\n・豊橋")
          embed11.add_field(name="-岐阜県-",value="・岐阜\n・高山")
          embed11.add_field(name="-静岡県-",value="・静岡\n・網代\n・三島\n・浜松")
        elif chiho == "近畿地方":
          embed11.add_field(name="-三重県-",value="・津\n・尾鷲")
          embed11.add_field(name="-大阪府-",value="・大阪")
          embed11.add_field(name="-兵庫県-",value="・神戸\n・豊岡")
          embed11.add_field(name="-京都府-",value="・京都\n・舞鶴")
          embed11.add_field(name="-滋賀県-",value="・大津\n・彦根")
          embed11.add_field(name="-奈良県-",value="・奈良\n・風屋")
        elif chiho == "中国/四国地方":
          embed11.add_field(name="-鳥取県-",value="・鳥取\n・米子")
          embed11.add_field(name="-島根県-",value="・松江\n・浜田\n・西郷")
          embed11.add_field(name="-岡山県-",value="・岡山\n・津山")
          embed11.add_field(name="-広島県-",value="・広島\n・庄原")
          embed11.add_field(name="-山口県-",value="・下関\n・山口\n・柳井\n・荻")
          embed11.add_field(name="-徳島県-",value="・徳島\n・日和佐")
          embed11.add_field(name="-香川県-",value="・高松")
          embed11.add_field(name="-愛媛県-",value="・松山\n・新居浜\n・宇和島")
          embed11.add_field(name="-高知県-",value="・高知\n・室戸岬\n・清水")
        elif chiho == "九州地方":
          embed11.add_field(name="-福岡県-",value="・福岡\n・八幡\n・飯塚\n・久留米")
          embed11.add_field(name="-大分県-",value="・大分\n・中津\n・日田\n・佐伯")
          embed11.add_field(name="-長崎県-",value="・長崎\n・佐世保\n・厳原\n・福江")
          embed11.add_field(name="-佐賀県-",value="・佐賀\n・伊万里")
          embed11.add_field(name="-熊本県-",value="・熊本\n・阿蘇乙姫\n・牛深\n・人吉")
          embed11.add_field(name="-宮崎県-",value="・宮崎\n・延岡\n・都城\n・高千穂")
          embed11.add_field(name="-鹿児島県-",value="・鹿児島\n・鹿屋\n・種子島\n・名瀬")
          embed11.add_field(name="-沖縄県-",value="・那覇\n・名護\n・久米島\n・南大東\n・宮古島\n・石垣島\n・与那国島")
        await message.channel.send(embed=embed11)
        command_log()
    
      else: 
        reg_res = re.compile(u"c!weather (.+)").search(message.content) 
        if reg_res: 
      
          if reg_res.group(1) in citycodes.keys(): 
        
            citycode = citycodes[reg_res.group(1)] 
            resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read() 
            resp = json.loads(resp.decode('utf-8')) 
        
            embed7 = discord.Embed(title="Weather",description=resp['location']['city'] + "の天気",color=0xabc9ec)
            for f in resp['forecasts']: 
              embed7.add_field(name=f['dateLabel'],value=f['telop'] + "\n")
            embed7.add_field(name='地方の情報',value=resp['description']['text'])
            await message.channel.send(embed=embed7)   
            command_log()
         
          else:
            await message.channel.send("その地域には対応していません")
            Command_log()
  
  # report
  if message.content.startswith("c!report"):
    text = message.content
    rep = text.strip("c!report ")
    await message.delete()
    embed6 = discord.Embed(title="ClariceBOT",description="report",color=0xabc9ec)
    embed6.add_field(name="レポート内容",value=rep)
    channel = client.get_channel(666148402433884162)
    await channel.send(embed=embed6)
    command_log()
  
  # ーーー 中間層 ーーー
  
  #1はグー、2はチョキ、3はパー
  if message.content == 'じゃんけん':
    janken = 1
    await message.channel.send('最初はぐー、じゃんけん…？\n`ぐー` : グーを出します\n`ちょき` : チョキを出します\n`ぱー` : パーを出します')
  if message.content == 'ぐー':
    janken = random.randint(1,3)
    guu_results = ['自分 : グー\nBOT : グー\n結果 : あいこ', '自分 : グー\nBOT : チョキ\n結果 : 勝ち', '自分 : グー\nBOT : パー\n結果 : 負け']
    await message.channel.send(guu_results[janken])
  if message.content == 'ちょき':
    janken = random.randint(1,3)
    choki_results = ['自分 : チョキ\nBOT : グー\n結果 : 負け', '自分 : チョキ\nBOT : チョキ\n結果 : あいこ', '自分 : チョキ\nBOT : パー\n結果 : 勝ち']
    await message.channel.send(choki_results[janken])
  if message.content == 'ぱー':
    janken = random.randint(1,3)
    paa_results = ['自分 : パー\nBOT : グー\n結果 : 勝ち', '自分 : パー\nBOT : チョキ\n結果 : 負け', '自分 : パー\nBOT : パー\n結果 : あいこ']
    await message.channel.send(paa_results[janken])  
    command_log()
        
  # ヘルプ
  if message.content == 'c!help':
    embed5 = discord.Embed(title="**Clarice BOT**",description="ヘルプ(0/5)",color=0xabc9ec)
    embed5.add_field(name="ヘルプ操作方法",value="下のリアクションを操作してください")
    
    embed4 = discord.Embed(title="**Clarice BOT**",description="ヘルプ(1/5)",color=0xabc9ec)
    embed4.add_field(name="c!say [`0~6`] [`text`]",value="textを匿名で発言します(0~6は無くても良い)")
    embed4.add_field(name="c!dict [`key`] [`value`]",value="辞書に登録します")
    embed4.add_field(name="c!dsay [`key`]",value="辞書に登録された対応するvalueを発言します")
    embed4.add_field(name="c!ddel [`key`]",value="辞書から指定された内容を削除します")
    embed4.add_field(name="おみくじ",value="おみくじを引けます")
    embed4.add_field(name="じゃんけん",value="じゃんけんしましょう！") 
         
    embed3 = discord.Embed(title="**Clarice BOT**",description="ヘルプ(2/5)",color=0xabc9ec)
    embed3.add_field(name="c!search [`検索対象`]",value="検索します")
    embed3.add_field(name="c!tl [`翻訳言語`] [`翻訳対象`]",value="翻訳します")
    embed3.add_field(name="c!ui / c!ui [`名前＃0000`]",value="送信者、または指定されたユーザー情報を表示します")
    embed3.add_field(name="c!avatar / c!avatar [`id`]",value="送信者、または指定されたユーザーのアイコン画像を表示します")
    embed3.add_field(name="c!dice",value="ダイスを振れます")
    embed3.add_field(name="c!weather",value="天気を調べられます")
      
    embed2 = discord.Embed(title="**Clarice BOT**",description="ヘルプ(3/5)",color=0xabc9ec) 
    embed2.add_field(name="c!report [`不具合等`]",value="不具合等の報告が出来ます")
    embed2.add_field(name="c!kick [`名前＃0000`]",value="メンバーを追放します`管理者権限が必要`")
    embed2.add_field(name="c!ban [`名前＃0000`]",value="メンバーを接続禁止にします`管理者権限が必要`")
    embed2.add_field(name="c!unban [`id`]",value="メンバーの接続禁止を解除します`管理者権限が必要`")
    embed2.add_field(name="c!servers",value="導入されたサーバーを調べます")
    embed2.add_field(name="c!guin / c!sein",value="送信元のサーバーの情報を表示します")      
          
    embed1 = discord.Embed(title="**Clarice BOT**",description="ヘルプ(4/5)",color=0xabc9ec)
    embed1.add_field(name="c!late",value="レイテンシを確認します")
    embed1.add_field(name="c!role [`オプション`]",value="役職について操作します")
    embed1.add_field(name="上記オプションについて",value="下記の情報は必須です")
    embed1.add_field(name="[`/a` / `/rm`]",value="役職を作成する場合 : `/a`\n役職を削除する場合 : `/rm`\n削除する場合は /rm [`役職ID`]")
    embed1.add_field(name="/aの場合",value="[`名前`] : 役職の名前\n[`0 ~ 3`] : 権限(3が最高権限)\n[`Tr/Fa`] : 別にロールメンバー表示\n[`Tr/Fa`] : メンション許可")
        
    den = client.guilds
    den1 = len(den)
    embed = discord.Embed(title="**Clarice BOT**",description="ヘルプ(5/5)",color=0xabc9ec)
    embed.add_field(name="`cb-log`チャンネル",value="ClariceBOT全体のログを表示します")
    embed.add_field(name="**導入サーバー数**",value=str(den1))
    embed.add_field(name="BOT起動時間",value="日によって変わります\n平日 `7時〜24時`\n休日 `10時〜26時`")
    embed.add_field(name="BOT導入(招待)",value="[ここをタップ(クリック)して導入！](https://discordapp.com/api/oauth2/authorize?client_id=642320951987535893&permissions=2015227095&scope=bot)")
    embed.add_field(name="総合サーバー",value="[ここをタップ(クリック)して参加！](https://discord.gg/jrUPRbc)")
    
    page_count = 0 #ヘルプの現在表示しているページ数 
    
    send_message = await message.channel.send(embed=embed18) #最初のページ投稿 
    command_log()
    await send_message.add_reaction("➡") 
    
    def help_react_check(reaction,user): 
      ''' ヘルプに対する、ヘルプリクエスト者本人からのリアクションかをチェックする  ''' 
      emoji = str(reaction.emoji) 
      if reaction.message.id != send_message.id: 
        return 0 
      if emoji == "➡" or emoji == "⬅": 
        if user != message.author: 
          return 0 
        else: 
          return 1 
          
    while not client.is_closed(): 
      try: 
        reaction,user = await client.wait_for('reaction_add',check=help_react_check,timeout=40.0) 
      except asyncio.TimeoutError: 
        return #時間制限が来たら、それ以降は処理しない 
      else: 
        emoji = str(reaction.emoji) 
        if emoji == "➡" and page_count < 5: 
          page_count += 1 
        if emoji == "⬅" and page_count > 0: 
          page_count -= 1 
        
        await send_message.clear_reactions() #事前に消去する 
        await send_message.delete()
        
        if page_count == 0: 
          send_message = await message.channel.send(embed=embed5) 
        elif page_count == 1: 
          send_message = await message.channel.send(embed=embed4)
        elif page_count == 2: 
          send_message = await message.channel.send(embed=embed3) 
        elif page_count == 3: 
          send_message = await message.channel.send(embed=embed2)
        elif page_count == 4:
          send_message = await message.channel.send(embed=embed1)  
        elif page_count == 5:
          send_message = await message.channel.send(embed=embed)    
          #各ページごとに必要なリアクション
         
        if page_count == 0: 
          await send_message.add_reaction("➡") 
        elif page_count == 1: 
          await send_message.add_reaction("⬅") 
          await send_message.add_reaction("➡") 
        elif page_count == 2: 
          await send_message.add_reaction("⬅") 
          await send_message.add_reaction("➡") 
        elif page_count == 3: 
          await send_message.add_reaction("⬅") 
          await send_message.add_reaction("➡") 
        elif page_count == 4: 
          await send_message.add_reaction("⬅") 
          await send_message.add_reaction("➡") 
        elif page_count == 5: 
          await send_message.add_reaction("⬅") 
          #各ページごとに必要なリアクション
  
# ループのスタート
loop.start()
          
# Botの起動とDiscordサーバーへの接続 
client.run(TOKEN)
