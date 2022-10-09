"""
Cog handling slash command configuring current channel for TTS.
All messages from configured channel will be read out.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.channel.source_channel import SourceChannel

HELP_MESSAGE = "`/source` - toggle all messages from current channel for TTS"


class SourceCog(Cog):
    def __init__(self, source_channel: SourceChannel) -> None:
        self._source_channel = source_channel

    @slash_command()
    async def source(self, interaction: CommandInteraction) -> None:
        """Toggle assignment of current channel for TTS"""
        channel_id = interaction.channel_id
        if channel_id in self._source_channel.get_channel_ids():
            self._source_channel.remove_channel_id(channel_id)
            await interaction.send("Channel removed")
        else:
            self._source_channel.add_channel_id(channel_id)
            await interaction.send("Channel added")
