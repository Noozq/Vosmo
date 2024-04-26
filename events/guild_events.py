async def on_guild_join(guild):
  from replit import db
  db[str(guild.id)] = '!'