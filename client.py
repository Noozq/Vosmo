import discord 
from discord.ext import commands 
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.default.all()

token = 

cliend = commands.Bot(command_prefix='!', intents = intents)

client.run(token)
