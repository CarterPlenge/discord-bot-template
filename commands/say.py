from discord import app_commands, Object, Interaction
from permissions import require_any_role
from ..logger import setup_logger

logger = setup_logger(__name__)

def register(tree: app_commands.CommandTree, database, discord_object: discord.Object):
    @tree.command(name="say", description="Makes the bot say what you type", guild=discord_object)
    @app_commands.describe(
        text="text",
    )
    async def say(interaction: Interaction, text: str):
        """The bot echoes what was input"""
        await interaction.response.send_message(
            text
        )
        logger.debug("Echo command executed.")
