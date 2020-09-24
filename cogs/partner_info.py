from discord.ext import commands
from datetime import datetime
import discord, json

skill_nt = nt("Skill", "name description awaken") # skill
frag_nt = nt("Frag", "min max awaken") # frag
step_nt = nt("Step", "min max awaken") # step
partner_nt = nt("Partner", "name resident frag step type skill image") # partner_info

with open("arcaea.json", "r", encoding="utf-8") as f:
  data = json.load(f) # 情報読み込み

# namedtupleに変換
pdata = list(map(lambda x: partner_nt(x[0], x[1], frag_nt(x[2][0], x[2][1], x[2][2]), step_nt(x[3][0], x[3][1], x[3][2]), x[4], skill_nt(x[5][0], x[5][1], x[5][2]), x[6]), data["partners"])) # partner_normal

class PartnerInfo(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    
  @bot.command()
  async def pinfo(ctx, *, name=None):
    
    # サーバーデータの読み込み
    with open("guild.json", "r", encoding="utf-8") as f:
      guilddata = json.load(f)
    
    # 送信されたメッセージの削除
    await ctx.message.edit(delete_after=3.0) 
    
    # 変数 'name' が指定されていない場合は…
    if name == None: 
      name = guilddata[str(ctx.guild.id)]["dataset"][1] if guilddata[str(ctx.guild.id)]["dataset"][1] != None else None 
    
    # 該当するパートナーを検索
    results = [l for l in pdata if name in i.name] 
    
    # 日本語
    if guilddata[str(ctx.guild.id)]["lang"] = "jpn":
   
      # 該当するパートナーが見つからない場合は…
      if len(results) == 0:
        return await ctx.send(embed=discord.Embed(title="パートナーが見つかりませんでした",color=0xFFDD00), delete_after=5.0) 
    
      # Embed 作成準備
      partner = results[0] 
      embed = discord.Embed(title=f"◇ パートナー名 {partner.name}",description=f"◇ タイプ {partner.type}",color=0x74596d) 
      embed.timestamp = datetime.utcnow() 
      embed.add_field(name="◇ FragとStep(最小値)",value=f"{partner.frag.min} | {partner.step.min}",inline=False) 
      embed.add_field(name="◇ FragとStep(最大値)",value=f"{partner.frag.max} | {partner.step.max}",inline=False) 
      embed.add_field(name="◇ FragとStep(覚醒後)",value=f"{partner.frag.awaken} | {partner.step.awaken}",inline=False) 
      embed.add_field(name=f"◇ Skill ({partner.skill.name})",value=f"{partner.skill.description}\n(覚醒後: {partner.skill.awaken})",inline=False) 
      embed.set_author(name="<Info> パートナーの情報 ",icon_url=bot.user.avatar_url) 
      embed.set_footer(text=f"送信者 : {ctx.author.name}") 
      embed.set_image(url=partner.image) 
   
    # 英語
    if guilddata[str(ctx.guild.id)]["lang"] = "eng":
   
      # 該当するパートナーが見つからない場合は…
      if len(results) == 0:
        return await ctx.send(embed=discord.Embed(title="No partner found.",color=0xFFDD00), delete_after=5.0) 
    
      # Embed 作成準備
      partner = results[0] 
      embed = discord.Embed(title=f"◇ Partner Name {partner.name}",description=f"◇ Type {partner.type}",color=0x74596d) 
      embed.timestamp = datetime.utcnow() 
      embed.add_field(name="◇ Frag, Step(minimum)",value=f"{partner.frag.min} | {partner.step.min}",inline=False) 
      embed.add_field(name="◇ Frag, Step(maximum)",value=f"{partner.frag.max} | {partner.step.max}",inline=False) 
      embed.add_field(name="◇ Frag, Step(awakened)",value=f"{partner.frag.awaken} | {partner.step.awaken}",inline=False) 
      embed.add_field(name=f"◇ Skill ({partner.skill.name})",value=f"{partner.skill.description}\n(覚醒後: {partner.skill.awaken})",inline=False) 
      embed.set_author(name="<Info> Partner Information ",icon_url=bot.user.avatar_url) 
      embed.set_footer(text=f"Author : {ctx.author.name}") 
      embed.set_image(url=partner.image)
  
    # Embed 送信
    await ctx.send(embed=embed,delete_after=60)
    
def setup(bot): bot.add_cog(PartnerInfo(bot))
