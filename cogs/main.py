from discord.ext import commands
from datetime import datetime
import discord, json

class Main(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    bot.remove_command("help")
    
  @commands.command()
  async def help(self, ctx):
    await ctx.message.edit(after_delete=3.0)
    with open("guild.json", "r", encoding="utf-8") as f:
      guilddata = json.load(f)
    if guilddata[str(ctx.guild.id)]["lang"] == "jpn":
      embed = discord.Embed(title="'a;<コマンド名>'で使用できます",color=0x74596d) 
      embed.timestamp = datetime.utcnow() 
      embed.add_field(name="help",value="ヘルプを表示します",inline=False) 
      embed.add_field(name="sinfo <曲名>",value="楽曲の情報を表示します",inline=False) 
      embed.add_field(name="pinfo <パートナー名>",value="パートナーの情報を表示します",inline=False) 
      embed.add_field(name="acsong (回数)",value="ランダムに楽曲を選びます",inline=False) 
      embed.add_field(name="acpartner",value="ランダムにパートナーを選びます",inline=False) 
      embed.add_field(name="set",value="設定パネルを表示します",inline=False) 
      embed.add_field(name="Other",value="BOTの導入は[こちら](https://discord.com/api/oauth2/authorize?client_id=702587324718120991&permissions=60480&scope=bot)",inline=False) 
      embed.set_author(name="ヘルプ",icon_url=self.bot.user.avatar_url) 
      embed.set_footer(text=f"送信者 : {ctx.author.name}")
    else:
      embed = discord.Embed(title="You can use the command with 'a;<command name>'.",color=0x74596d) 
      embed.timestamp = datetime.utcnow() 
      embed.add_field(name="help",value="Show you help.",inline=False) 
      embed.add_field(name="sinfo <曲名>",value="Get song information.",inline=False) 
      embed.add_field(name="pinfo <パートナー名>",value="Get partner information.",inline=False) 
      embed.add_field(name="acsong (回数)",value="Bot randomly chooses song.",inline=False) 
      embed.add_field(name="acpartner",value="Bot randomly chooses partner.",inline=False) 
      embed.add_field(name="set",value="Show you setting panel.",inline=False) 
      embed.add_field(name="Other",value="Click [here](https://discord.com/api/oauth2/authorize?client_id=702587324718120991&permissions=60480&scope=bot) for bot introduction.",inline=False) 
      embed.set_author(name="Help",icon_url=self.bot.user.avatar_url) 
      embed.set_footer(text=f"Author : {ctx.author.name}")
    await ctx.send(embed=e,delete_after=60)
    
  @self.bot.event
  async def on_ready(self): 
    embed = discord.Embed(title="<Ready> ArcaeaSupportBotが起動しました",color=0xBCF946) 
    embed.timestamp = datetime.utcnow() 
    embed.set_author(name="起動ログ",icon_url=self.bot.user.avatar_url) 
    embed.set_footer(text="ver.2.0")
    channel = bot.get_channel(723600070284673036) 
    await channel.send(embed=embed) 
    print("<Ready> 起動しました")
    
    for g in self.bot.guilds:
      with open("guild.json", "r", encoding="utf-8") as f:
        guilddata = json.load(f)
      if str(g.id) in guilddata: 
        lang = guilddata[str(g.id)]["lang"]
        del guilddata[str(g.id)]
      else: lang = "eng"
      data = {
        "lang":lang,
        "song":{
          "ignorepacks":[], 
          "ignoresongs":[], 
          "levels":[[], [], [], []], 
          "side":None, 
          "illustrators":[], 
          "composers":[], 
          "chart_creators":[], 
          "notes_limit":[[0,1600], [0,1600], [0,1600], [0,1600]], 
          "constant_limit":[[1.0,12.0], [1.0,12.0], [1.0,12.0], [1.0,12.0]]
        } 
        "partner":{
          "resident":"all", 
          "step_limit":[[0,200], [0,200]], 
          "frag_limit":[[0,200], [0,200]], 
          "types":[], 
          "skills":[]
        }
      }
      guilddata.setdefault(str(g.id), data)
      with open("guild.json", "w", encoding="utf-8") as f:
        json.dump(guiktddata, f)
    print("<Success> サーバーデータの設定が完了しました")
             
def setup(bot): bot.add_cog(Main(bot))
