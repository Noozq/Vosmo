import discord
from discord.ext import commands

class Removerole_Command(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def removerole(self, ctx, role: discord.Role, member: discord.Member):
    await member.remove_roles(role)
    await ctx.send(f"Rolle {role.name} wurde {member.mention} entfernt.")

async def setup(client):
  await client.add_cog(Removerole_Command(client))