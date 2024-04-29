import discord
from discord.ext import commands
from replit import db

class Remove_Reaction_Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remove_reaction_role(self, ctx, message_id: int, emoji: str):
        """Entfernt eine Reaktionsrolle für eine bestimmte Nachricht.

        Args:
            message_id (int): Die ID der Nachricht, aus der die Reaktionsrolle entfernt werden soll.
            emoji (str): Das Emoji der Reaktionsrolle, die entfernt werden soll.
        """
        reaction_roles = db.get("reaction_roles", {})
        if str(message_id) in reaction_roles:
            message_roles = reaction_roles[str(message_id)]
            if emoji in message_roles:
                del message_roles[emoji]
                db["reaction_roles"] = reaction_roles
                if not message_roles:
                    del reaction_roles[str(message_id)]
                    db["reaction_roles"] = reaction_roles
                await ctx.send(f"Reaktionsrolle für Emoji {emoji} erfolgreich von Nachricht {message_id} entfernt.")
            else:
                await ctx.send("Die angegebene Reaktionsrolle wurde nicht gefunden.")
        else:
            await ctx.send("Keine Reaktionsrollen für diese Nachricht gefunden.")

async def setup(client):
    await client.add_cog(Remove_Reaction_Command(client))