import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = discord.Client(intents=discord.Intents.default())
openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.content}]
    )
    await message.channel.send(response["choices"][0]["message"]["content"])

client.run(DISCORD_BOT_TOKEN)
