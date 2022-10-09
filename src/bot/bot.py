"""
Module creating the bot, adding all required Cogs.
"""

from os import environ

from disnake import Intents
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv

from bot.channel.sources import SourceChannels
from bot.channel.target import TargetChannel
from bot.command.help import HelpCog
from bot.command.list import ListCog
from bot.command.read import ReadCog
from bot.command.source import SourceCog
from bot.command.target import TargetCog
from bot.event.on_application_command import OnApplicationCommandCog
from bot.event.on_message import OnMessageCog
from bot.event.on_ready import OnReadyCog
from bot.speaker import Speaker
from bot.tts_scheduler import TtsScheduler

load_dotenv()
DISCORD_BOT_TOKEN = environ["DISCORD_BOT_TOKEN"]


def prepare_and_run_bot() -> None:
    bot = InteractionBot(intents=_prepare_intents())
    source_channels = SourceChannels()
    target_channel = TargetChannel(bot)
    speaker = Speaker(target_channel)
    tts_scheduler = TtsScheduler(bot.loop, speaker)
    bot.add_cog(OnApplicationCommandCog())
    bot.add_cog(OnReadyCog(target_channel))
    bot.add_cog(OnMessageCog(bot, tts_scheduler, source_channels))
    bot.add_cog(SourceCog(source_channels))
    bot.add_cog(TargetCog(target_channel))
    bot.add_cog(ReadCog(tts_scheduler, target_channel))
    bot.add_cog(ListCog(bot, source_channels, target_channel))
    bot.add_cog(HelpCog())
    bot.run(token=DISCORD_BOT_TOKEN)


def _prepare_intents() -> Intents:
    intents = Intents().default()
    intents.message_content = True
    return intents
