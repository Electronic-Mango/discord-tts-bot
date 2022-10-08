from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.speaker import Speaker


class TargetCog(Cog):
    def __init__(self, speaker: Speaker) -> None:
        super().__init__()
        self._speaker = speaker

    @slash_command()
    async def target(self, interaction: CommandInteraction) -> None:
        """Command setting current channel as TTS target"""
        await interaction.response.defer()
        if self._speaker.is_target_channel(channel_id := interaction.channel_id):
            await self._speaker.clear_target_channel()
            await interaction.send("Current channel unset as target")
        else:
            await self._speaker.set_target_channel(channel_id)
            await interaction.send("Current channel set as target")
