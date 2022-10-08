"""
Module creating the bot, adding all required Cogs.
"""

from disnake import Client, Intents
from disnake.ext.commands import InteractionBot

from bot.command.source import SourceCog
from bot.command.target import TargetCog
from bot.event.on_message import OnMessageCog
from bot.event.on_ready import OnReadyCog
from bot.speaker import Speaker
from bot.tts_scheduler import TtsScheduler


def prepare_bot() -> Client:
    bot = InteractionBot(intents=_prepare_intents())
    speaker = Speaker(bot)
    tts_scheduler = TtsScheduler(bot.loop, speaker)
    bot.add_cog(OnReadyCog(bot, speaker))
    bot.add_cog(on_message := OnMessageCog(bot, tts_scheduler))
    bot.add_cog(SourceCog(on_message))
    bot.add_cog(TargetCog(speaker))
    return bot


def _prepare_intents() -> Intents:
    intents = Intents().default()
    intents.message_content = True
    return intents
