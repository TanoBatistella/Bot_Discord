import discord
import json

with open('config/config.json') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.run(config['token'])
