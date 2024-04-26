import discord
from replit import db
from discord.ext import commands 
from dotenv import load_dotenv
import os


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
  await ctx.send(f"Prefix changed to {prefix}")
  
@client.command()
async def show_allprefixes(ctx):
  prefixes = "Server Präfixe:\n"
  for key in db.keys():
      if key.isdigit():
          server_id = key
          prefix = db[key]
          prefixes += f"ServerID: `{server_id}` | Prefix `{prefix}`\n"
  if prefixes == "Server Präfixe:\n":
    await ctx.send("No prefixes found.")
    
  await ctx.send(prefixes)

if __name__ == '__main__':
  client.run(token)
  
      