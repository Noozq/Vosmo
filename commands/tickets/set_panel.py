import discord
from discord.ext import commands
import json

class TicketCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.load_config()

    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.ticket_category_id = config['ticket_category_id']

    @commands.Cog.listener()
    async def on_ready(self):
        print('TicketCog is ready')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.client.user and user != self.client.user:
            if str(reaction.emoji) == "🎫":
                # Perform your action here, for example, create a ticket
                guild = reaction.message.guild
                category = discord.utils.get(guild.categories, id=self.ticket_category_id)

                ticket_channel = await category.create_text_channel(name=f'ticket-{user.name}', 
                                                                    topic=f'Opened by {user.name}')

                await user.send(f'Your ticket has been created in {ticket_channel.mention}')
                ticket_message = await ticket_channel.send('test')
                await ticket_message.add_reaction('🔒')
                await ticket_message.add_reaction('🔓')
                await ticket_message.add_reaction('⛔️')
                await ticket_message.add_reaction('✅')

    @commands.command()
    async def send_ticket_message(self, ctx):
        message = await ctx.send("React to this message with 🎫 to create a ticket.")
        await message.add_reaction("🎫")

async def setup(client):
    await client.add_cog(TicketCog(client))
from replit import db
from replit import db
