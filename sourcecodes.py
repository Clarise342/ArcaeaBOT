import discord
import os
from discord.ext import commands

TOKEN = "NzA1NDE0MzA0NzY5NTA3Mzc4.Xqra_g.BxW75f-ChK0cg6hyv40M6JU9kIo"
bot = commands.Bot(command_prefix="sc/")

@bot.command()
async def search(ctx, lang):
  if lang in ["py","js","rb","java","php","json"]:
    print("a")

bot.run(TOKEN)
