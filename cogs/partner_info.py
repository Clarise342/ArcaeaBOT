from discord.ext import commands

class PartnerInfo(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    
def setup(bot): bot.add_cog(PartnerInfo(bot))
