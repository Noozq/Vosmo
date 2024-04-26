import discord
from replit import db
from discord.ext import commands 
from dotenv import load_dotenv
import os

# LISTENER IMPORTS
from events.guild_events import on_guild_join


# SETTING
def get_prefix(client, message):
  default_prefix = "!"
  server_id = str(message.guild.id)
  return db.get(server_id, default_prefix)


load_dotenv()
intents = discord.Intents.all()
token = os.getenv("TOKEN")
bot_version = "0.1.0"

client = commands.Bot(command_prefix=get_prefix, intents = intents)



# LISTENER

client.add_listener(on_guild_join)

@client.event
async def on_ready():

  #COMMANDS 

  #SETTINGS
  for filename in os.listdir('commands/tickets'):
    if filename.endswith('.py'):
      await client.load_extension(f'commands.tickets.{filename[:-3]}')
      
  db["version"] = "bot_version"
  print(
    f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃      {client.user} - {client.user.id} - {bot_version}       ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    '''
    )
  print(f'{client.user}')
  
  
@client.command()
async def set_prefix(ctx, prefix : str):
  server_id = str(ctx.guild.id)
  db[server_id] = prefix
  embed = discord.Embed(description=f"Prefix set to {prefix}\n")
  await ctx.send(embed = embed)
  
@client.command()
@commands.is_owner()
async def show_prefixes(ctx):
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

if __name__ == '__main__':
  client.run(token)
  
      