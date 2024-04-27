import discord
from replit import db
from discord.ext import commands

class Joinrole_Command(commands.Cog):
    def __init__(self, client):
        self.client = client

   # SET JOIN ROLE
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_joinrole(self, ctx, *, role: discord.Role):
        if ctx.author.guild_permissions.administrator:
            db['join_role'] = role.id
            embed = discord.Embed(description=f"Joinrole set to {role.mention}\n")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You don't have permission to use this command.")
            await ctx.send(embed=embed)

    @commands.command()
    async def show_roles(self, ctx):
        if "join_role" in db:
            join_role_id = db["join_role"]
            join_role = ctx.guild.get_role(join_role_id)
            if join_role:
                await ctx.send(f"Join-Rolle: {join_role.mention}")
            else:
                await ctx.send("Die gespeicherte Join-Rolle wurde nicht gefunden.")
        else:
            await ctx.send("Es wurde keine Join-Rolle gespeichert.")

    @commands.command()
    async def remove_join_role(self, ctx):
        if "join_role" in db:
            del db["join_role"]
            await ctx.send("Die gespeicherte Join-Rolle wurde entfernt.")
        else:
            await ctx.send("Es wurde keine Join-Rolle gespeichert.")


async def setup(client):
    await client.add_cog(Joinrole_Command(client))