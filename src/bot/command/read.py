"""
Cog handling "read" command.
This command is in two forms:
 1. Direct slash command
 2. Context-menu message command
Both will schedule given text for TTS.
"""

from disnake import CommandInteraction, Message
from disnake.ext.commands import Cog, Param, message_command, slash_command

from bot.tts_scheduler import TtsScheduler


class ReadCog(Cog):
    def __init__(self, tts_scheduler: TtsScheduler) -> None:
        self._tts_scheduler = tts_scheduler

    @slash_command(name="read")
    async def slash_read(
        self,
        interaction: CommandInteraction,
        text: str = Param(name="text", description="text to read"),
    ) -> None:
        """Read out given text"""
        await self._read(interaction, text)

    @message_command(name="read")
    async def message_read(
        self,
        interaction: CommandInteraction,
        message: Message,
    ) -> None:
        """Read out given text"""
        await self._read(interaction, message.content)

    async def _read(self, interaction: CommandInteraction, text: str) -> None:
        if stripped_text := text.strip():
            await interaction.send("Reading...")
            self._tts_scheduler.add_message(stripped_text)
        else:
            await interaction.send("No text to read out!")
