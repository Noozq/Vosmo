import discord
from discord.ext import commands
from replit import db

class Help_Command(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def help(self, ctx):
    for key in db.keys():
      if key.isdigit():
        prefix = db[key]
        embed = discord.Embed(title = 'Alle Vosmo Commands!', description = f'\n '
                              f'Prefix : {prefix}\n', color=discord.Color.red())
        await ctx.send(embed=embed)

async def setup(client):
  await client.add_cog(Help_Command(client))