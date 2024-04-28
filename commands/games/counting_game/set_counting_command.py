import discord
from discord.ext import commands

class Set_Counting_Command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.current_game = None
        self.current_number = 1
        self.rewards = {}  # Belohnungen für bestimmte Zahlen

    @commands.command()
    async def start_counting_game(self, ctx):
        if self.current_game is None:
            self.current_game = ctx.channel
            self.current_number = 1
            await self.current_game.send('Ein neues Counting Game wurde gestartet! Gebt Zahlen in aufsteigender Reihenfolge ab.')
        else:
            await ctx.send('Ein Spiel läuft bereits!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_reward(self, ctx, number: int, *, reward: str):
        # Überprüfen, ob der Benutzer bereits eine Belohnung für diese Zahl festgelegt hat
        if number in self.rewards:
            await ctx.send(f"Es existiert bereits eine Belohnung für die Zahl {number}. Möchtest du sie aktualisieren?")
            try:
                reply = await self.client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
                if reply.content.lower() == "ja":
                    self.rewards[number] = reward
                    await ctx.send(f"Belohnung für die Zahl {number} wurde erfolgreich aktualisiert.")
                else:
                    await ctx.send("Belohnungsaktualisierung abgebrochen.")
            except asyncio.TimeoutError:
                await ctx.send("Zeitüberschreitung. Belohnungsaktualisierung abgebrochen.")
        else:
            self.rewards[number] = reward
            await ctx.send(f"Belohnung für die Zahl {number} wurde erfolgreich festgelegt.")

    @commands.command()
    async def show_rewards(self, ctx):
        if self.rewards:
            rewards_list = "\n".join([f"Zahl: {number} - Belohnung: {reward}" for number, reward in self.rewards.items()])
            await ctx.send(f"Aktuell festgelegte Belohnungen:\n{rewards_list}")
        else:
            await ctx.send("Es wurden noch keine Belohnungen festgelegt.")

    async def clear_channel(self, channel):
        async for message in channel.history(limit=None):
            if not message.pinned:
                await message.delete()

    async def give_reward(self, number, member):
        # Belohnung für die gegebene Zahl überprüfen und dem Mitglied geben
        if number in self.rewards:
            reward = self.rewards[number]
            # Hier kannst du die Belohnung für das Mitglied implementieren
            await member.send(f"Glückwunsch! Du hast die Zahl {number} erreicht und erhältst die Belohnung: {reward}")

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

                    # Überprüfen, ob eine Belohnung für die erreichte Zahl festgelegt wurde
                    await self.give_reward(number, message.author)

                else:
                    await message.add_reaction('❌')
                    await message.channel.send('Das Counting Game wurde beendet!\n'
                                               f'\nDie richtige Zahl war: **{self.current_number - 1}**\n'
                                               f'starte neu mit `start_counting_game`\n')
                    self.current_game = None
                    self.current_number = 1
                    await self.clear_channel(message.channel)

async def setup(client):
    await client.add_cog(Set_Counting_Command(client))