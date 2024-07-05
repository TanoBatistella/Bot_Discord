from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tirar(self, ctx, dado: str):
        try:
            tiradas, limite = map(int, dado.split('d'))
        except Exception:
            await ctx.send('El formato debe ser NdN, por ejemplo, 2d6')
            return
        
        resultados = [str(random.randint(1, limite)) for _ in range(tiradas)]
        resultado = ', '.join(resultados)
        total = sum(map(int, resultados))
        await ctx.send(f'Resultados: {resultado}. Total: {total}')

async def setup(bot):
    await bot.add_cog(Fun(bot))
