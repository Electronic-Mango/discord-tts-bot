from os import environ

from disnake import FFmpegPCMAudio, Intents, PCMVolumeTransformer, VoiceClient
from disnake.ext.commands import Bot
from disnake.message import Message
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

DISCORD_BOT_TOKEN = environ["DISCORD_BOT_TOKEN"]
TEXT_LANGUAGE = environ["TEXT_LANGUAGE"]
SOURCE_CHANNEL_IDS = list(map(int, environ["SOURCE_CHANNEL_IDS"].split(",")))
TARGET_CHANNEL_ID = int(environ["TARGET_CHANNEL_ID"])
VOICE_FILE_PATH = environ.get("VOICE_FILE_PATH", "voice_file.mp3")

intents = Intents().default()
intents.message_content = True
bot = Bot(intents=intents)


@bot.event
async def on_message(message: Message) -> None:
    if message.channel.id not in SOURCE_CHANNEL_IDS or not (text := message.content):
        return
    voice_client = await get_voice_client()
    speech = gTTS(text, lang=TEXT_LANGUAGE)
    speech.save(VOICE_FILE_PATH)
    audio_source = PCMVolumeTransformer(FFmpegPCMAudio(VOICE_FILE_PATH))
    voice_client.play(audio_source)


async def get_voice_client() -> VoiceClient:
    voice_channel = bot.get_channel(TARGET_CHANNEL_ID)
    for voice_client in bot.voice_clients:
        if voice_client.channel == voice_channel:
            return voice_client
    return await voice_channel.connect()


bot.run(token=DISCORD_BOT_TOKEN)
