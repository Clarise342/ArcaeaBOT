from discord.ext import commands

class AutoChooseSong(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
def setup(bot): bot.add_cog(AutoChooseSong(bot))
