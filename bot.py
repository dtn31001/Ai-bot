import os
import discord
import openai
from discord.ext import commands

# Lấy biến môi trường từ Railway
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Kiểm tra token
if not DISCORD_BOT_TOKEN:
    raise ValueError("⚠️ DISCORD_BOT_TOKEN không được tìm thấy trong biến môi trường!")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY không được tìm thấy trong biến môi trường!")

# Cấu hình bot
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập thành công với tên: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.content}]
    )
    await message.channel.send(response["choices"][0]["message"]["content"])

# Chạy bot
if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
