from discord import app_commands, Object, Interaction
from permissions import require_any_role

def register(tree: app_commands.CommandTree, database, guild_id: int):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="say", description="Makes the bot say what you type", guild=guild)
    @require_any_role("admin", "mod")
    @app_commands.describe(
        text="text",
    )
    async def say(interaction: Interaction, text: str):
        await interaction.response.send_message(
            text
        )