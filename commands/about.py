from discord import app_commands, Object, Interaction
from ..logger import setup_logger

logger = setup_logger(__name__)

def register(tree: app_commands.CommandTree, database, guild_id: int):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="about", description="About this bot", guild=guild)
    async def about(interaction: Interaction):
        """Prints info about the bot"""
        
        message = """
        This bot was made using a template from
        https://github.com/CarterPlenge/discord-bot-template
        
        This command has not been reconfigured from the template default. 
        """
        
        await interaction.response.send_message(
            message,
            ephemeral=True
        )
        logger.debug("Executed about command")
