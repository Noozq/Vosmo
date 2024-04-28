import discord 
from discord.ext import commands

class Info_Command(commands.Cog):
  def __init__(self, client):
    self.client = client

  
  @commands.command()
  async def info(self, ctx, arg="bot"):
      if arg.lower() == "bot":
          owner = "noozq" # LINCENS 
          embed = discord.Embed(title="Bot Information", description="Hier sind einige Informationen über den Bot:", color=0x00ff00)
          embed.add_field(name="Name", value=self.client.user.name, inline=False)
          embed.add_field(name="ID", value=self.client.user.id, inline=False)
          embed.add_field(name="Besitzer", value=f'{owner}', inline=False)
          await ctx.send(embed=embed)
      elif arg.lower() == "server":
          guild = ctx.guild
          embed = discord.Embed(title="Server Information", description="Hier sind einige Informationen über den Server:", color=0x00ff00)
          embed.add_field(name="Name", value=guild.name, inline=False)
          embed.add_field(name="ID", value=guild.id, inline=False)
          embed.add_field(name="Besitzer", value=guild.owner, inline=False)
          embed.add_field(name="Mitgliederzahl", value=guild.member_count, inline=False)
          await ctx.send(embed=embed)
      elif arg.lower() == "mod":
          mods = [member for member in ctx.guild.members if member.guild_permissions.administrator]
          mod_list = '\n'.join([str(mod) for mod in mods])
          embed = discord.Embed(title="Moderator Information", description="Hier sind einige Informationen über die Moderatoren auf diesem Server:", color=0x00ff00)
          embed.add_field(name="Moderatoren", value=mod_list, inline=False)
          await ctx.send(embed=embed)
      else:
          await ctx.send("Ungültiges Argument. Bitte verwende `!info bot`, `!info server` oder `!info mod`.")
        
async def setup(client):
  await client.add_cog(Info_Command(client))