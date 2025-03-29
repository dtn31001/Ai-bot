import os
import discord
import requests
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

@client.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập thành công với tên: {client.user}")

@client.command()
async def ask(ctx, *, user_input: str = None):
    if not user_input:
        await ctx.send("⚠️ Vui lòng nhập câu hỏi sau lệnh !ask")
        return
    
    if "bạn được tạo từ ai" in user_input.lower():
        await ctx.send("Tôi được tạo ra bởi Đỗ Anh Tuấn.")
        return
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": user_input}]}
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ Không nhận được phản hồi từ API.")
        await ctx.send(reply)
    except Exception as e:
        print(f"❌ Lỗi OpenAI API: {e}")
        await ctx.send("⚠️ Bot gặp lỗi khi gọi API OpenAI. Hãy thử lại sau!")

# Chạy bot
if __name__ == "__main__":
    print("🔄 Đang khởi động bot...")
    print(f"🔑 Token được sử dụng: {'Có' if DISCORD_BOT_TOKEN else 'Không có'}")
    client.run(DISCORD_BOT_TOKEN)
