import client
from discord.ext import commnds


class Create_panel(commands.Cog):
  def __init__(self, client):
    self.client = client
  
async def setup(client):
  await client.add_cog(Create_panel(client))