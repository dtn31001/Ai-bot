import os
import discord
import requests
from discord.ext import commands

# URL API để lấy API Key
API_KEY_SERVER_URL = "http://195.179.229.119/gpt/api.php?api_key_request=true"

# Hàm lấy API Key từ server
def get_openai_api_key():
    try:
        response = requests.get(API_KEY_SERVER_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("api_key", None)
    except requests.RequestException as e:
        print(f"⚠️ Lỗi khi lấy API Key: {e}")
        return None

# Lấy API Key từ server
OPENAI_API_KEY = get_openai_api_key()

# Lấy biến môi trường từ Railway
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Kiểm tra token
if not DISCORD_BOT_TOKEN:
    raise ValueError("⚠️ DISCORD_BOT_TOKEN không được tìm thấy trong biến môi trường!")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY không được lấy từ server!")

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
        api_url = f"http://195.179.229.119/gpt/api.php?prompt={requests.utils.quote(user_input)}&api_key={requests.utils.quote(OPENAI_API_KEY)}&model=gpt-3.5-turbo"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        reply = data.get("response", "⚠️ Không nhận được phản hồi từ API.")
        await ctx.send(reply)
    except requests.RequestException as e:
        print(f"❌ Lỗi OpenAI API: {e}")
        await ctx.send("⚠️ Bot gặp lỗi khi gọi API OpenAI. Hãy thử lại sau!")

# Chạy bot
if __name__ == "__main__":
    print("🔄 Đang khởi động bot...")
    print(f"🔑 Token được sử dụng: {'Có' if DISCORD_BOT_TOKEN else 'Không có'}")
    client.run(DISCORD_BOT_TOKEN)
