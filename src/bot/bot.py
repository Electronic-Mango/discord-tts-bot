"""
Module creating the bot, adding all required Cogs and running it.
"""

from os import getenv

from disnake import Client, Intents
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv

from bot.event.on_message import OnMessage
from bot.event.on_ready import OnReady
from bot.speaker import Speaker
from bot.tts_scheduler import TtsScheduler

load_dotenv()
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")


def prepare_bot() -> Client:
    bot = InteractionBot(intents=_prepare_intents())
    speaker = Speaker(bot)
    tts_scheduler = TtsScheduler(bot.loop, speaker)
    bot.add_cog(OnReady(bot, speaker))
    bot.add_cog(OnMessage(bot, tts_scheduler))
    return bot


def _prepare_intents() -> Intents:
    intents = Intents().default()
    intents.message_content = True
    return intents
