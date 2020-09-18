from discord.ext import commands

class SongInfo(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
def setup(bot): bot.add_cog(SongInfo(bot))
