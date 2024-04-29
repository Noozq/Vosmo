import discord
from discord.ext import commands
from replit import db

class Show_Reaction_Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['show'])
    async def show_reaction_roles(self, ctx, message_id: int = None):
        """Zeigt die gespeicherten Reaktionsrollen für eine bestimmte Nachricht oder alle Nachrichten an.

        Args:
            message_id (int, optional): Die ID der Nachricht. Wenn nicht angegeben, werden alle gespeicherten Reaktionsrollen angezeigt.
        """
        reaction_roles = db.get("reaction_roles", {})
        if message_id:
            message_roles = reaction_roles.get(str(message_id))
            if message_roles:
                embed = discord.Embed(title=f"Gespeicherte Reaktionsrollen für Nachricht {message_id}", color=0x00ff00)
                for emoji, role_id in message_roles.items():
                    role = discord.utils.get(ctx.guild.roles, id=role_id)
                    if role:
                        embed.add_field(name=f"Reaktion: {emoji}", value=f"Rolle: {role.name}", inline=False)
                    else:
                        embed.add_field(name=f"Reaktion: {emoji}", value="Rolle nicht gefunden", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Keine gespeicherten Reaktionsrollen für diese Nachricht.")
        else:
            if reaction_roles:
                embed = discord.Embed(title="Gespeicherte Reaktionsrollen für alle Nachrichten", color=0x00ff00)
                for message_id, message_roles in reaction_roles.items():
                    description = ""
                    for emoji, role_id in message_roles.items():
                        role = discord.utils.get(ctx.guild.roles, id=role_id)
                        if role:
                            description += f"Reaktion: {emoji}, Rolle: {role.name}\n"
                        else:
                            description += f"Reaktion: {emoji}, Rolle nicht gefunden\n"
                    embed.add_field(name=f"Nachricht {message_id}", value=description, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Keine gespeicherten Reaktionsrollen vorhanden.")

async def setup(client):
    await client.add_cog(Show_Reaction_Command(client))