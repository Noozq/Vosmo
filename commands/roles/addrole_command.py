import discord
from discord.ext import commands

class Addrole_Command(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def addrole(self, ctx, role: discord.Role, member: discord.Member):
    await member.add_roles(role)
    await ctx.send(f"Rolle {role.name} wurde {member.mention} hinzugefügt.")

async def setup(client):
  await client.add_cog(Addrole_Command(client))