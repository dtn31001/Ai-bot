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

# Cấu hình bot với intents mở rộng
intents = discord.Intents.default()
intents.messages = True  # Bật quyền đọc tin nhắn
intents.message_content = True  # Bật quyền đọc nội dung tin nhắn
client = commands.Bot(command_prefix="!", intents=intents)
openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập thành công với tên: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower().startswith("!ask"):
        user_input = message.content[5:].strip()
        if not user_input:
            await message.channel.send("⚠️ Vui lòng nhập câu hỏi sau lệnh !ask")
            return
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            print(f"❌ Lỗi OpenAI API: {e}")
            await message.channel.send("⚠️ Bot gặp lỗi khi gọi API OpenAI. Hãy thử lại sau!")
    else:
        await message.channel.send("🤖 Xin chào! Hãy dùng lệnh `!ask` để hỏi tôi.")

# Chạy bot
if __name__ == "__main__":
    print("🔄 Đang khởi động bot...")
    print(f"🔑 Token được sử dụng: {'Có' if DISCORD_BOT_TOKEN else 'Không có'}")
    client.run(DISCORD_BOT_TOKEN)
