"""
Cog handling slash command setting current channel as TTS output.
Messages from configured source channels will be read out here.
"""

from disnake import CommandInteraction
from disnake.enums import ChannelType
from disnake.ext.commands import Cog, slash_command

from bot.speaker import Speaker

HELP_MESSAGE = "`/target` - toggle current **voice** channel as TTS output"


class TargetCog(Cog):
    def __init__(self, speaker: Speaker) -> None:
        self._speaker = speaker

    @slash_command()
    async def target(self, interaction: CommandInteraction) -> None:
        """Set current voice channel as TTS output"""
        await interaction.response.defer()
        channel = interaction.channel
        if channel.type != ChannelType.voice:
            await interaction.send("Can only be used in voice channels!", ephemeral=True)
        elif self._speaker.is_target_channel(channel.id):
            await self._speaker.clear_target_channel()
            await interaction.send("Current channel unset as target")
        else:
            await self._speaker.set_target_channel(channel.id)
            await interaction.send("Current channel set as target")
