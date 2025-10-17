from discord import app_commands, Object, Interaction
from permissions import require_any_role

def register(tree: app_commands.CommandTree, database, guild_id: int):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="health-check", description="Check bot and db health ", guild=guild)
    @require_any_role("admin", "mod")
    async def health_check(interaction: Interaction):
        success = database.test_connection()
        
        if success:
            await interaction.response.send_message(
                "Database connection is healthy",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Database connection failed",
                ephemeral=True
            )