"""
Cog handling slash command listing all configured channels.
All source and target channels are listed.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.event.on_message import OnMessageCog
from bot.speaker import Speaker

HELP_MESSAGE = "`/list` - list all configured channels"


class ListCog(Cog):
    def __init__(self, speaker: Speaker, on_message: OnMessageCog) -> None:
        self._speaker = speaker
        self._on_message = on_message

    @slash_command()
    async def list(self, interaction: CommandInteraction) -> None:
        """List all configured channels"""
        await interaction.response.defer()
        target_channel = self._speaker.get_target_channel()
        source_channels = self._on_message.get_source_channels()
        response = f"Target: {target_channel}\n\nSources:\n{source_channels}"
        await interaction.send(response)
