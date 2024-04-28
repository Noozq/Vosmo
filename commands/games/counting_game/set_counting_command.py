import discord
from discord.ext import commands
from replit import db

class Set_Counting_Command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.current_game = None
        self.current_number = 1

    @commands.command()
    async def start_counting_game(self, ctx):
        if self.current_game is None:
            self.current_game = ctx.channel
            self.current_number = 1
            await self.current_game.send('Ein neues Counting Game wurde gestartet! Gebt Zahlen in aufsteigender Reihenfolge ab.')
        else:
            await ctx.send('Ein Spiel läuft bereits!')

    async def clear_channel(self, channel):
        async for message in channel.history(limit=None):
            if not message.pinned:
                await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.isdigit():
            number = int(message.content)
            if self.current_game and message.channel == self.current_game:
                if number == self.current_number:
                    self.current_number += 1
                    await message.add_reaction('✅')
                else:
                    for key in db.keys():
                        if key.isdigit():
                            server_id = key
                            prefix = db[key]
                            await message.add_reaction('❌')
                            await message.channel.send('Das Counting Game wurde beendet!'
                                                       f'\nDie richtige Zahl war: {self.current_number - 1}'
                                                       f'starte neu mit `{prefix}start_counting_game`')
                            self.current_game = None
                            self.current_number = 1
                            await self.clear_channel(message.channel)

async def setup(client):
    await client.add_cog(Set_Counting_Command(client))