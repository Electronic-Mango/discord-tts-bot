"""
Module creating the bot, adding all required Cogs.
"""

from os import environ

from disnake import Client, Intents
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv

from bot.channel.source_data import SourceChannelData
from bot.channel.target_channel import TargetChannel
from bot.channel.target_data import TargetChannelData
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


def prepare_and_run_bot() -> Client:
    bot = InteractionBot(intents=_prepare_intents())
    source_channel_data = SourceChannelData()
    target_channel = TargetChannel(bot)
    target_channel_data = TargetChannelData(target_channel)
    speaker = Speaker(target_channel)
    tts_scheduler = TtsScheduler(bot.loop, speaker)
    bot.add_cog(OnApplicationCommandCog())
    bot.add_cog(OnReadyCog(target_channel_data))
    bot.add_cog(OnMessageCog(bot, tts_scheduler, source_channel_data))
    bot.add_cog(SourceCog(source_channel_data))
    bot.add_cog(TargetCog(target_channel_data))
    bot.add_cog(ReadCog(tts_scheduler))
    bot.add_cog(ListCog(bot, source_channel_data, target_channel_data))
    bot.add_cog(HelpCog())
    bot.run(token=DISCORD_BOT_TOKEN)


def _prepare_intents() -> Intents:
    intents = Intents().default()
    intents.message_content = True
    return intents
