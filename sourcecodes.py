import discord
import os
import sys
from discord.ext import commands 

bot = commands.Bot(command_prefix="sc/")
token = os.environ['TOKEN']

@bot.command()
async def search(ctx, lang):
  if lang in ["py","js","rb","java","php","json"]:
    print("a")

@bot.command()
async def exit(ctx):
  await bot.logout()
  await sys.exit()

bot.run(token)
