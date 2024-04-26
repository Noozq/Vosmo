import discord
from discord.ext import commands
from replit import db


class Prefixes_Commands(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def set_prefix(self, ctx, prefix : str):
    server_id = str(ctx.guild.id)
    db[server_id] = prefix
    embed = discord.Embed(description=f"Prefix set to {prefix}\n")
    await ctx.send(embed = embed)

  @commands.command()
  async def reset_prefix(self, ctx):
    server_id = str(ctx.guild.id)
    db[server_id] = "!"
    embed = discord.Embed(description=f"Prefix reset to !\n")
    await ctx.send(embed = embed)

  
  @commands.command()
  @commands.is_owner()
  async def show_prefixes(self, ctx):
      embed = discord.Embed(title="Server Präfixe", color=discord.Color.red())

      found_prefixes = False
      for key in db.keys():
          if key.isdigit():
              server_id = key
              prefix = db[key]
              embed.add_field(name=f"ServerID : {server_id}", value=f"Präfix: `{prefix}`", inline=False)
              found_prefixes = True

      if not found_prefixes:
          embed.description = "Es sind keine Server-Präfixe gespeichert."

      await ctx.send(embed=embed)


async def setup(client):
  await client.add_cog(Prefixes_Commands(client))
