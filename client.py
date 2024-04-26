import discord
from replit import db
from discord.ext import commands 
from dotenv import load_dotenv
from colorama import Fore, Back, Style
import os

# LISTENER IMPORTS
from events.guild_events import on_guild_join
from events.join_events import on_member_join

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
client.add_listener(on_member_join)

@client.event
async def on_ready():

  #COMMANDS 

  for filename in os.listdir('commands/tickets'):
    if filename.endswith('.py'):
      await client.load_extension(f'commands.tickets.{filename[:-3]}')

  for filename in os.listdir('commands/settings'):
    if filename.endswith('.py'):
      await client.load_extension(f'commands.settings.{filename[:-3]}')

  for filename in os.listdir('commands/roles'):
    if filename.endswith('.py'):
      await client.load_extension(f'commands.roles.{filename[:-3]}')

  

  print(
    Fore.BLUE + f"{client.user}" + Fore.BLACK + " -- " + Fore.BLUE + f"{client.user.id}" + Fore.BLACK + " -- " + Fore.BLUE + f"{bot_version}" + Fore.BLACK + " -- " + Fore.BLUE + f"{db['prefix']}"
  )

if __name__ == '__main__':
  client.run(token)