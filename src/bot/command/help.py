"""
Command Cog sending back a help message.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.command.list import HELP_MESSAGE as LIST_HELP_MESSAGE
from bot.command.read import HELP_MESSAGE as READ_HELP_MESSAGE
from bot.command.source import HELP_MESSAGE as SOURCE_HELP_MESSAGE
from bot.command.target import HELP_MESSAGE as TARGET_HELP_MESSAGE

_ALL_HELP_MESSAGES = [
    LIST_HELP_MESSAGE,
    READ_HELP_MESSAGE,
    SOURCE_HELP_MESSAGE,
    TARGET_HELP_MESSAGE,
]
_FULL_HELP_MESSAGE = "\n".join(_ALL_HELP_MESSAGES)


class HelpCog(Cog):
    @slash_command()
    async def help(self, interaction: CommandInteraction) -> None:
        """Get help information for the bot"""
        await interaction.send(_FULL_HELP_MESSAGE, ephemeral=True)
