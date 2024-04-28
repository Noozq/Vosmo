import discord
from discord.ext import commands
from replit import db

class Help_Command(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def help(self, ctx):
        embed = discord.Embed(title = 'Alle Vosmo Commands!', description = f' ', color=discord.Color.red())
        embed.add_field(name = 'Info', value = '`-`', inline = False)
        embed.add_field(name = 'Moderation', value = '`-`', inline = False)
        embed.add_field(name = 'Fun', value = '`start_counting_game` `start_quiz` ', inline = False)
        embed.add_field(name = 'Settings', value = '`help` `set_prefix` `reset_prefix` `show_prefixes(owner)` ', inline = False)
        await ctx.send(embed=embed)

async def setup(client):
  await client.add_cog(Help_Command(client))