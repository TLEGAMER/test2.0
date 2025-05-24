from flask import Flask
from threading import Thread
import discord
from discord.ext import commands, tasks
import asyncio

# ------------------ Keep Alive ------------------
app = Flask(__name__)


@app.route('/')
def home():
    return "I'm alive!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# ------------------ Discord Bot ------------------
TOKEN = "MTM3MTU4MDY0NjE1MzEzMDAyNA.GzYs97.JDqjeWycvn60wNzNoGhg_o3dBO8UiWmgrpkqNw"
VOICE_CHANNEL_ID = 1375227595741855825

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    await connect_to_voice_channel()
    voice_check.start()  # เริ่ม Task ตรวจสอบการเชื่อมต่อ


async def connect_to_voice_channel():
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        if not bot.voice_clients or not bot.voice_clients[0].is_connected():
            try:
                await channel.connect(self_mute=True, self_deaf=True)
                print(f"📢 Joined voice channel: {channel.name}")
            except discord.ClientException:
                print("⚠️ Already connected or unable to connect.")
            except Exception as e:
                print(f"❌ Error connecting to voice channel: {e}")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and after.channel is None:
        print("🔄 Bot got disconnected, retrying...")
        await asyncio.sleep(3)
        await connect_to_voice_channel()


@tasks.loop(seconds=30)
async def voice_check():
    """Task ตรวจสอบทุก 30 วินาที ถ้าเด้งจะเข้าใหม่อัตโนมัติ"""
    if not bot.voice_clients or not bot.voice_clients[0].is_connected():
        print("🔁 Bot not connected, attempting to reconnect...")
        await connect_to_voice_channel()


# ✅ เรียก Keep-Alive ก่อนรันบอท
keep_alive()
bot.run(TOKEN)
