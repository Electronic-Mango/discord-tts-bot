"""
Cog handling "read" command.
This command is in two forms:
 1. Direct slash command
 2. Context-menu message command
Both will schedule given text for TTS.
"""

from disnake import CommandInteraction, Message
from disnake.ext.commands import Cog, Param, message_command, slash_command

from bot.channel.target import TargetChannel
from bot.tts_scheduler import TtsScheduler

HELP_MESSAGE = "`/read <text>` - read out given text"


class ReadCog(Cog):
    def __init__(self, tts: TtsScheduler, target_channel: TargetChannel) -> None:
        self._tts_scheduler = tts
        self._target_channel = target_channel

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
        if not self._target_channel.is_connected():
            await interaction.send("Target channel is not set!", ephemeral=True)
        elif stripped_text := text.strip():
            await interaction.send("Reading...", ephemeral=True)
            self._tts_scheduler.add_message(stripped_text)
        else:
            await interaction.send("No text to read out!", ephemeral=True)
