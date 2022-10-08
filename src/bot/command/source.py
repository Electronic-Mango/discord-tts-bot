"""
Cog handling slash command configuring current channel for TTS.
All messages from configured channel will be read out.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.event.on_message import OnMessageCog

HELP_MESSAGE = "`/source` - toggle all messages from current channel for TTS"


class SourceCog(Cog):
    def __init__(self, on_message_cog: OnMessageCog) -> None:
        self._on_message_cog = on_message_cog

    @slash_command()
    async def source(self, interaction: CommandInteraction) -> None:
        """Toggle assignment of current channel for TTS"""
        channel_id = interaction.channel_id
        if self._on_message_cog.is_source_channel_id(channel_id):
            self._on_message_cog.remove_source_channel_id(channel_id)
            await interaction.send("Channel removed")
        else:
            self._on_message_cog.add_source_channel_id(channel_id)
            await interaction.send("Channel added")
