import discord
from discord import app_commands, Object, Interaction, ActivityType, Activity, Status
from logger import setup_logger

logger = setup_logger(__name__)

def register(tree: app_commands.CommandTree, discord_object: discord.Object):
    @tree.command(name="status", description="Set the bot status and activity", guild=discord_object)
    @app_commands.describe(
        status="The status to set (online, idle, dnd, invisible)",
        activity_type="The type of activity (playing, streaming, listening, watching, competing)",
        activity="The activity name/text"
    )
    @app_commands.choices(
        status=[
            app_commands.Choice(name="online", value="online"),
            app_commands.Choice(name="idle", value="idle"),
            app_commands.Choice(name="dnd", value="dnd"),
            app_commands.Choice(name="invisible", value="invisible")
        ],
        activity_type=[
            app_commands.Choice(name="playing", value="playing"),
            app_commands.Choice(name="streaming", value="streaming"),
            app_commands.Choice(name="listening", value="listening"),
            app_commands.Choice(name="watching", value="watching"),
            app_commands.Choice(name="competing", value="competing")
        ]
    )
    async def status(interaction: Interaction, status: str, activity_type: str = None, activity: str = None):
        """Set the bot's status and optional activity"""
        
        status_map = {
            "online": Status.online,
            "idle": Status.idle,
            "dnd": Status.do_not_disturb,
            "invisible": Status.invisible
        }
        
        activity_type_map = {
            "playing": ActivityType.playing,
            "streaming": ActivityType.streaming,
            "listening": ActivityType.listening,
            "watching": ActivityType.watching,
            "competing": ActivityType.competing
        }
        
        try:
            activity_obj = None
            if activity_type and activity:
                activity_obj = Activity(
                    name=activity,
                    type=activity_type_map.get(activity_type, ActivityType.playing)
                )

            await interaction.client.change_presence(
                status=status_map.get(status, Status.online),
                activity=activity_obj
            )
            
            activity_text = f" with activity: **{activity}** ({activity_type})" if activity_obj else ""
            await interaction.response.send_message(
                f"Bot status set to **{status}**{activity_text}",
                ephemeral=True
            )
            logger.debug(f"Status command executed.")
        except Exception as e:
            await interaction.response.send_message(
                f"Error setting status: {str(e)}",
                ephemeral=True
            )
            logger.error(f"Status command failed. {str(e)}")