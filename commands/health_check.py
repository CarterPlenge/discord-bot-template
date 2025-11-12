from discord import app_commands, Object, Interaction
from permissions import require_any_role
from ..logger import setup_logger

logger = setup_logger(__name__)

def register(tree: app_commands.CommandTree, database, guild_id: int):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="health-check", description="Check bot and db health ", guild=guild)
    async def health_check(interaction: Interaction):
        """Sends a message containing the database's current status"""
        success = database.test_connection()
        
        if success:
            await interaction.response.send_message(
                "Database connection is healthy",
                ephemeral=True
            )
            logger.debug("health-check command passed")
        else:
            await interaction.response.send_message(
                f"Database connection failed",
                ephemeral=True
            )
            logger.debug("health-check command failed.")
