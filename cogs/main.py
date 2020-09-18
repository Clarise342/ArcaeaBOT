from discord.ext import commands
from datetime import datetime
import discord

class Main(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    bot.remove_command("help")
    
  @commands.command()
  async def help(self, ctx):
    
    
  @self.bot.event
  async def on_ready(self): 
    embed = discord.Embed(title="<Ready> ArcaeaSupportBotが起動しました",color=0xBCF946) 
    embed.timestamp = datetime.utcnow() 
    embed.set_author(name="起動ログ",icon_url=self.bot.user.avatar_url) 
    embed.set_footer(text="ver.2.0")
    channel = bot.get_channel(723600070284673036) 
    await channel.send(embed=embed) 
    print("<Ready> 起動しました")
    
def setup(bot): bot.add_cog(Main(bot))
