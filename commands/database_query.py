from discord import app_commands, Object, Interaction
from permissions import require_any_role
from datetime import datetime

def register(tree, database, guild_id):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="database-query", description="Query the database for information", guild=guild)
    @app_commands.describe(
        databasequery="What do you want to query for?"
    )
    @app_commands.choices(
        databasequery=[
            app_commands.Choice(name="gameRequest", value="gameRequest")
        ]
    )
    async def database_query(interaction: Interaction, databasequery: str):
        try:
            if databasequery == "gameRequest":
                status, response = database.get_game_requests(guild_id)
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

                    created_str = created_at.strftime("%Y-%m-%d %H:%M")

                    formatted.append(
                        f"Game: {row['game']} | on: {row['platform']} | UserID: {row['username']} | Time: {created_str}"
                    )



                output = "\n".join(formatted)

                # Prevent messages > 2000 characters; discord enforces this
                if len(output) > 1900:
                    output = "Templete command: " + output[:1900] + "\n... (truncated)"

                await interaction.response.send_message(f"```{output}```")

        except Exception as e:
            await interaction.response.send_message(
                f"An unexpected error occurred: {str(e)}",
                ephemeral=True
            )