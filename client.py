import discord 
from discord.ext import commands 
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.all()
token = os.getenv("TOKEN")

client = commands.Bot(command_prefix='!', intents = intents)


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
  async def set_language(ctx, language : str):
    
        
if __name__ == '__main__':
    client.run(token)
