from discord.ext import commands
import sys
import discord
import os 

token = os.environ['TOKEN']
extension = [
  'cogs.bot_event',
  'cogs.fun_dict',
  'cogs.many_command'
] 

class ArcaeaSupportBot(commands.Bot): 
  def __init__(self, command_prefix): 
    super().__init__(command_prefix)
    for cog in extension: 
      try: 
        self.load_extension(cog) 
      except Exception: 
        print(f"<Error> A error occurred in cog '{cog}'.") 
      else: 
        print("<Success> Cog '{cog}' loading is complete.") 
    
if __name__ == '__main__': 
  bot = ArcaeaSupportBot(command_prefix="a") 
  
  @bot.command(name="reload",aliases=["r"]) 
  async def system_reload(ctx): 
    await ctx.message.delete() 
    if ctx.author.id == 536506865883021323: 
      for cog in extension: 
        try: bot.unload_extension(cog) 
        except Exception: pass 
        finally: 
          try: bot.load_extension(cog) 
          except Exception as e: 
            print(f"<Error> Error info:\n{e}") 
            await msg.edit(embed=discord.Embed(title=f"<Error> A error occurred in cog '{cog}'.",color=0xFF0000),delete_after=3.0)
          else: await ctx.send(embed=discord.Embed(title=f"<Success> Cog '{cog}' reloading is complete.",color=0x00FF2D),delete_after=1.0) 
      await ctx.send(embed=discord.Embed(title="<Complete> All cogs were finished reloading.",color=0x00FF2D), delete_after=3.0)
    else: await ctx.send(embed=discord.Embed(title="<Error> You don't have permissions.",color=0xFF0000), delete_after=3.0)
      
bot.run(token)
