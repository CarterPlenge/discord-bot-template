from discord import app_commands, Object, Interaction
from channel import require_channel
from sql_manager import SQLManager

database = SQLManager()

def register(tree: app_commands.CommandTree, database, guild_id: int):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="request", description="Request a new game", guild=guild)
    @app_commands.describe(
        game="The game you want to request.",
        platform="The platform the game is on."
    )
    @app_commands.choices(
        platform=[
            app_commands.Choice(name="PC (work in progress)", value="PC"),
            app_commands.Choice(name="Xbox", value="Xbox"),
            app_commands.Choice(name="Playstation", value="Playstation"),
            app_commands.Choice(name="Switch", value="Switch")
        ]
    )
    async def request(interaction: Interaction, game: str, platform: app_commands.Choice[str]):
        platform_value = platform.value if isinstance(platform, app_commands.Choice) else platform
        
        success, message = database.add_game_request(interaction.user.id, game, platform_value)
        
        if success:
            response = ""
            if platform_value == "PC":
                response = "\n\nWe are still in the process of getting our steam PC Cafe liceses. Ask the esport director for more info."
            
            await interaction.response.send_message(
                f"Templete command: Your request for **{game}** on **{platform_value}** has been received.{response}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Error: {message}",
                ephemeral=True
            )