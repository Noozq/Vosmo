import discord
import json
import os
from discord.ext import commands
import random

class Set_Emojiquiz_Command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.emojis = ["🍎", "🍌", "🍒", "🍓", "🍇", "🍍", "🥭", "🍋", "🥝", "🍈"]  # Vorgefertigte Emojis
        self.load_data()

    def load_data(self):
        if not os.path.exists("emojis.json"):
            self.emoji_data = {}
        else:
            with open("emojis.json", "r") as f:
                self.emoji_data = json.load(f)

    def save_data(self):
        with open("emojis.json", "w") as f:
            json.dump(self.emoji_data, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.emoji_data[str(guild.id)] = {}
        self.save_data()

    @commands.command()
    async def add_word(self, ctx, word: str):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.emoji_data:
            self.emoji_data[guild_id] = {}

        if len(word) > len(self.emojis):
            await ctx.send("Es gibt nicht genug Emojis für dieses Wort.")
            return

        emoji_word = ""
        for i, char in enumerate(word):
            emoji_word += f"{self.emojis[i]}{char} "

        self.emoji_data[guild_id][word] = emoji_word.strip()
        self.save_data()
        await ctx.send(f"Wort '{word}' erfolgreich hinzugefügt.")

    @commands.command()
    async def start_quiz(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.emoji_data:
            await ctx.send("Es wurden noch keine Wörter für dieses Server hinzugefügt.")
            return

        difficulty = self.get_difficulty(guild_id)
        word, emoji_word = self.get_random_word_and_emojis(guild_id)
        await ctx.send(f"Errate das Wort basierend auf den Emojis (Schwierigkeitsstufe: {difficulty}):")
        message = await ctx.send(emoji_word)

        # Speichere das aktuelle Wort und die Nachrichten-ID für den Hinweis
        self.current_word = word
        self.message_id = message.id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.message_id:
            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if str(payload.emoji) == "❓":
                await message.channel.send(f"Hier ist ein Hinweis: {self.current_word[0]}{'-' * (len(self.current_word) - 1)}")

    def get_difficulty(self, guild_id):
        # Hier könnte man die Schwierigkeitsstufe pro Server speichern und zurückgeben
        # Für dieses Beispiel wird immer "Leicht" zurückgegeben
        return "Leicht"

    def get_random_word_and_emojis(self, guild_id):
        word = random.choice(list(self.emoji_data[guild_id].keys()))
        emoji_word = self.emoji_data[guild_id][word]
        return word, emoji_word

async def setup(client):
    await client.add_cog(Set_Emojiquiz_Command(client))