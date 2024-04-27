import discord
from discord.ext import commands

class Help_Command(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def help(self, ctx):
    embed = discord.Embed(title="Help Command", color=discord.Color.red())
    await ctx.send(embed=embed)

async def setup(client):
  await client.add_cog(Help_Command(client))