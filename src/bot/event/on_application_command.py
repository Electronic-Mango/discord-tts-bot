"""
Event Cog logging information about called command.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog
from loguru import logger


class OnApplicationCommandCog(Cog):
    @Cog.listener()
    async def on_application_command(self, interaction: CommandInteraction) -> None:
        source = f"[{interaction.guild or 'DM'}] [{interaction.channel}]"
        user = interaction.author
        command = interaction.application_command.qualified_name
        logger.info(f"{source} [{user}] [{command}]")
