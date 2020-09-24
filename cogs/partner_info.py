from discord.ext import commands
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
    with open("guild.json", "r", encoding="utf-8") as f:
      guilddata = json.load(f)
    await ctx.message.edit(delete_after=3.0) 
    if name == None: name = guilddata[str(ctx.guild.id)]["dataset"][1] if guilddata[str(ctx.guild.id)]["dataset"][1] != None else None 
    partners = [i for i in pdata if name in i.name] 
    if len(partners) == 0: return await ctx.send("パートナーが見つかりませんでした", delete_after=5.0) 
    partner = partners[0] 
    e = discord.Embed(title=f"◆ パートナー名 {partner.name}",description=f"◇ タイプ {partner.type}",color=0x74596d) 
    e.timestamp = dt.utcnow() 
    e.add_field(name="◇ FragとStep(最小値)",value=f"{partner.frag.min} | {partner.step.min}",inline=False) 
    e.add_field(name="◇ FragとStep(最大値)",value=f"{partner.frag.max} | {partner.step.max}",inline=False) 
    e.add_field(name="◇ FragとStep(覚醒後)",value=f"{partner.frag.awaken} | {partner.step.awaken}",inline=False) 
    e.add_field(name=f"◇ Skill ({partner.skill.name})",value=f"{partner.skill.description}\n(覚醒後: {partner.skill.awaken})",inline=False) 
    e.set_author(name=" パートナーの情報 ",icon_url=bot.user.avatar_url) 
    e.set_footer(text=f"送信者 : {ctx.author.name}") 
    e.set_image(url=partner.image) 
    await ctx.send(embed=e,delete_after=60)
    
def setup(bot): bot.add_cog(PartnerInfo(bot))
