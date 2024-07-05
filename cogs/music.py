from discord.ext import commands
import discord
import youtube_dl
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
            else:
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send("No estás en un canal de voz.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("No estoy en un canal de voz.")

    @commands.command()
    async def play(self, ctx, *, query):
        async with ctx.typing():
            if ctx.voice_client is None:
                await self.join(ctx)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0', 
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(query, download=False)
                    if 'entries' in info:
                        url = info['entries'][0]['url']
                    else:
                        url = info['url']

                    source = await discord.FFmpegOpusAudio.from_probe(url)
                    ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))
                    await ctx.send(f"Reproduciendo: {info['title']}")

            except Exception as e:
                await ctx.send(f"Error al intentar reproducir: {str(e)}")

    def play_next(self, ctx):
        if self.queue:
            next_url = self.queue.pop(0)
            asyncio.run_coroutine_threadsafe(self.play(ctx, query=next_url), self.bot.loop)

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Pausado.")
        else:
            await ctx.send("No hay música reproduciéndose actualmente.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Reanudado.")
        else:
            await ctx.send("No hay música pausada actualmente.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Canción saltada.")
        else:
            await ctx.send("No hay música reproduciéndose actualmente.")

async def setup(bot):
    await bot.add_cog(Music(bot))
