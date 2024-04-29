import discord
from discord.ext import commands
from replit import db

class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.client.get_guild(payload.guild_id)
        if guild is None:
            return

        message_id = str(payload.message_id)
        reaction_roles = db.get("reaction_roles", {})
        if message_id in reaction_roles:
            emoji = str(payload.emoji)
            if emoji in reaction_roles[message_id]:
                role_id = reaction_roles[message_id][emoji]
                role = discord.utils.get(guild.roles, id=role_id)
                if role is not None:
                    member = guild.get_member(payload.user_id)
                    if member is not None:
                        await member.add_roles(role)
                        print(f"Gave role {role.name} to {member.display_name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.client.get_guild(payload.guild_id)
        if guild is None:
            return

        message_id = str(payload.message_id)
        reaction_roles = db.get("reaction_roles", {})
        if message_id in reaction_roles:
            emoji = str(payload.emoji)
            if emoji in reaction_roles[message_id]:
                role_id = reaction_roles[message_id][emoji]
                role = discord.utils.get(guild.roles, id=role_id)
                if role is not None:
                    member = guild.get_member(payload.user_id)
                    if member is not None:
                        await member.remove_roles(role)
                        print(f"Removed role {role.name} from {member.display_name}")
                        
    @commands.command()
    async def set_reaction_role(self, ctx, message_id: int, emoji: str, role: discord.Role):
        """Setzt eine Reaktionsrolle für eine bestimmte Nachricht.

        Args:
            message_id (int): Die ID der Nachricht, auf die die Reaktion gesetzt werden soll.
            emoji (str): Das Emoji, auf das reagiert werden soll.
            role (discord.Role): Die Rolle, die zugewiesen werden soll.
        """
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Die Nachricht wurde nicht gefunden.")
            return

        await message.add_reaction(emoji)

        reaction_roles = db.get("reaction_roles", {})
        message_roles = reaction_roles.get(str(message_id), {})
        message_roles[emoji] = role.id
        reaction_roles[str(message_id)] = message_roles
        db["reaction_roles"] = reaction_roles
        await ctx.send(f"Reaktionsrolle für Emoji {emoji} erfolgreich für Nachricht {message_id} gesetzt")

async def setup(client):
    await client.add_cog(ReactionRoles(client))