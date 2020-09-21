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
    
def setup(bot): bot.add_cog(PartnerInfo(bot))
