"""
Cog handling slash command setting current channel as TTS output.
Messages from configured source channels will be read out here.
"""

from disnake import CommandInteraction
from disnake.enums import ChannelType
from disnake.ext.commands import Cog, slash_command

from bot.channel.target_data import TargetChannelData

HELP_MESSAGE = "`/target` - toggle current **voice** channel as TTS output"


class TargetCog(Cog):
    def __init__(self, target_channel_data=TargetChannelData) -> None:
        self._target_channel_data = target_channel_data

    @slash_command()
    async def target(self, interaction: CommandInteraction) -> None:
        """Set current voice channel as TTS output"""
        await interaction.response.defer()
        channel = interaction.channel
        if channel.type != ChannelType.voice:
            await interaction.send("Use only in voice channels!", ephemeral=True)
        elif self._target_channel_data.get_channel_id() == channel.id:
            await self._target_channel_data.unset_channel_id()
            await interaction.send("Current channel unset as target")
        else:
            await self._target_channel_data.set_channel_id(channel.id)
            await interaction.send("Current channel set as target")
