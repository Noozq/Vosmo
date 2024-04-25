import discord
from replit import db
from discord.ext import commands 
from dotenv import load_dotenv
import os


# SETTING
def get_prefix(client, message):
  default_prefix = "!"
  return db.get("prefix", default_prefix)
  
load_dotenv()
intents = discord.Intents.all()
token = os.getenv("TOKEN")

client = commands.Bot(command_prefix=get_prefix, intents = intents)


@client.event
async def on_ready():
  print(
    f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃    {client.user} - {client.user.id} - {version}     ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    '''
    )
  print(f'{client.user}')
  for filename in os.listdir('commands/tickets'):
    if filename.endswith('.py'):
      await client.load_extension(f'commands.tickets.{filename[:-3]}')
  
@client.command()
async def set_prefix(ctx, prefix : str):
  db["prefix"] = prefix
  await ctx.send(f"Prefix changed to {prefix}")
  
@client.command()
async def save_data(ctx, key, value):
  db[key] = value
  await ctx.send(f'Daten mit Key "{key}" und Wert "{value}" gespeichert.')

# Command zum Anzeigen von Daten aus der Replit DB
@client.command()
async def show_data(ctx, key):
  value = db.get(key)
  if value:
    await ctx.send(f'Der Wert für den Key "{key}" lautet: {value}')
  else:
    await ctx.send(f'Keine Daten für den Key "{key}" gefunden.')
    
        
if __name__ == '__main__':
    client.run(token)
