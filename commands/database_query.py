import discord
from discord import app_commands, Object, Interaction
from permissions import require_any_role
from datetime import datetime
from logger import setup_logger

logger = setup_logger(__name__)


# Prevent messages > 2000 characters; discord enforces this
MAX_MESSAGE_LENGTH = 1900
DATE_FORMATE = "%Y-%m-%d %H:%M"


def register(tree: app_commands.CommandTree, database, discord_object: discord.Object):
    @tree.command(name="database-query", description="Query the database for information", guild=discord_object)
    @app_commands.describe(
        databasequery="What do you want to query for?"
    )
    @app_commands.choices(
        databasequery=[
            app_commands.Choice(name="gameRequest", value="gameRequest")
        ]
    )
    async def database_query(interaction: Interaction, databasequery: str):
        """Handle database querys"""
        try:
            if databasequery == "gameRequest":
                status, response = database.get_game_requests(discord_object.id)
                if not status:
                    raise Exception(response)
                
                if not response:
                    await interaction.response.send_message(
                        "No game requests found.", ephemeral=True
                    )
                    return

                formatted = []
                for row in response:
                    created_at = row["created_at"]

                    created_str = created_at.strftime(DATE_FORMATE)

                    formatted.append(
                        f"Game: {row['game']} | on: {row['platform']} | UserID: {row['username']} | Time: {created_str}"
                    )
                    
                output = "\n".join(formatted)

                # Prevent messages > 2000 characters; discord enforces this
                if len(output) > MAX_MESSAGE_LENGTH:
                    output = "Templete command: " + output[:MAX_MESSAGE_LENGTH] + "\n... (truncated)"

                await interaction.response.send_message(f"```{output}```")
                logger.debug("Database query command passed")

        except Exception as e:
            await interaction.response.send_message(
                f"An unexpected error occurred: {str(e)}",
                ephemeral=True
            )
            logger.debug(f"Database query command failed. {str(e)}")