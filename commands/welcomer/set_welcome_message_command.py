import discord
from discord.ext import commands
from replit import db

class Set_Welcome_Message_Command(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def set_welcome_message(self, ctx, *, message):
    if ctx.author.guild_permissions.administrator:
      db['welcome_message'] = message
      embed = discord.Embed(description=f"Welcome Message set to:\n{message}")
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(description="You don't have permission to use this command.")
      await ctx.send(embed=embed)

  @commands.command()
  async def show_welcome_message(self, ctx):
    if 'welcome_message' in db:
      welcome_message = db['welcome_message']
      await ctx.send(f"Welcome Message:\n{welcome_message}")
    else:
      await ctx.send("No welcome message set.")

async def setup(client):
  await client.add_cog(Set_Welcome_Message_Command(client))