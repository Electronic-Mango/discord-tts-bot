from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command, Param

from bot.tts_scheduler import TtsScheduler


class ReadCog(Cog):
    def __init__(self, tts_scheduler: TtsScheduler) -> None:
        self._tts_scheduler = tts_scheduler

    @slash_command()
    async def read(
        self,
        interaction: CommandInteraction,
        text: str = Param(name="text", description="text to read"),
    ) -> None:
        """Read out given text"""
        await interaction.send("Reading...")
        self._tts_scheduler.add_message(text)
