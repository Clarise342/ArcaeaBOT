from discord.ext import commands
import discord, json

class AutoChoosePartner(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
def setup(bot): bot.add_cog(AutoChoosePartner(bot))
