from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def borrar(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)  
        await ctx.send(f'{amount} mensajes han sido borrados.', delete_after=5)

    @borrar.error
    async def borrar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No tienes permisos para usar este comando.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
