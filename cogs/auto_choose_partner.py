from discord.ext import commands
import discord, json

artwork_nt = nt("Artwork", "normal beyond") # artwork
level_nt = nt("Level", "PAST PRESENT FUTURE BEYOND") # レベル
notes_nt = nt("Notes", "PAST PRESENT FUTURE BEYOND") # ノーツ数
constant_nt = nt("Constant", "PAST PRESENT FUTURE BEYOND") # 譜面定数
chart_nt = nt("ChartDesigner", "PAST PRESENT FUTURE BEYOND") # 譜面製作者
tags_nt = nt("Tags", "composer illustrator chartdesigner")
song_nt = nt("Song", "name side pack artwork bpm composer illustrator chart tags level notes constant") # song_info


with open("arcaea.json", "r", encoding="utf-8") as f: 
  data = json.load(f) # 情報読み込み

# namedtupleに変換
sdata = list(map(lambda x: song_nt(x[0], x[1], x[2], artwork_nt(x[3][0], x[3][1]), x[4], x[5], x[6], chart_nt(x[7][0], x[7][1], x[7][2], x[7][3]), tags_nt(x[8][0], x[8][1], x[8][2]), level_nt(x[9][0], x[9][1], x[9][2], x[9][3]), notes_nt(x[10][0],x[10][1],x[10][2],x[10][3]), constant_nt(x[11][0],x[11][1],x[11][2],x[11][3])), data["songs"])) # song

class AutoChoosePartner(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
def setup(bot): bot.add_cog(AutoChoosePartner(bot))
