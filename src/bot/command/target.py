"""
Cog handling slash command setting current channel as TTS output.
Messages from configured source channels will be read out here.
"""

from disnake import CommandInteraction
from disnake.enums import ChannelType
from disnake.ext.commands import Cog, slash_command

from bot.channel.target import TargetChannel

HELP_MESSAGE = "`/target` - toggle current **voice** channel as TTS output"


class TargetCog(Cog):
    def __init__(self, target_channel: TargetChannel) -> None:
        self._target_channel = target_channel

    @slash_command()
    async def target(self, interaction: CommandInteraction) -> None:
        """Set current voice channel as TTS output"""
        await interaction.response.defer()
        channel = interaction.channel
        if channel.type != ChannelType.voice:
            await interaction.send("Use only in voice channels!", ephemeral=True)
        elif self._target_channel.get_channel_id() == channel.id:
            await self._target_channel.disconnect()
            await interaction.send("Current channel unset as target")
        else:
            await self._target_channel.connect(channel.id)
            await interaction.send("Current channel set as target")
