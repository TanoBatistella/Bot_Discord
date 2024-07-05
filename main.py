import discord
from discord.ext import commands
import json
import os
import asyncio
from utils.database import create_table, get_last_greeting, update_last_greeting
from utils.helpers import get_weather_message
from datetime import datetime

create_table()

with open('config/config.json') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')  
                print(f'Cargada la extensión: {filename}')
            except Exception as e:
                print(f'Error al cargar la extensión {filename}: {str(e)}')


@bot.event
async def on_ready():
    print(f'El bot está listo. Conectado como {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  

    if message.guild and message.channel.name == 'general':
        last_greeting_date = get_last_greeting(message.author.id)
        if last_greeting_date is None or last_greeting_date != datetime.now().date().isoformat():
            weather_message = get_weather_message(message.author)
            greeting_message = await message.channel.send(f'Buenos días {message.author.mention}, bienvenido al servidor. Que la pases muy bien. {weather_message}')
            update_last_greeting(message.author.id)
            await asyncio.sleep(6)  
            await greeting_message.delete()

    await bot.process_commands(message)  

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['token'])

if __name__ == "__main__":
    asyncio.run(main())
