import discord
from discord import app_commands, Object, Interaction
from logger import setup_logger

logger = setup_logger(__name__)

def register(tree: app_commands.CommandTree, discord_object: discord.Object):

    @tree.command(name="about", description="About this bot", guild=discord_object)
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
