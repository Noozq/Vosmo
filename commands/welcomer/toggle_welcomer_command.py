import discord 
from discord.ext import commands
from replit import db

class Toggle_Welcomer_Command(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def toggle_welcomer(self, ctx):
    if ctx.author.guild_permissions.administrator:
      if "welcome_message_enabled" in db:
        del db["welcome_message_enabled"]
        embed = discord.Embed(description="Welcome Message deaktiviert.")
        await ctx.send(embed=embed)
      else:
        db["welcome_message_enabled"] = True
        embed = discord.Embed(description="Welcome Message aktiviert.")
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(description="You don't have permission to use this command.")
      await ctx.send(embed=embed)

async def setup(client):
  await client.add_cog(Toggle_Welcomer_Command(client))