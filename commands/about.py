from discord import app_commands, Object, Interaction

def register(tree: app_commands.CommandTree, database, guild_id: int):
    guild = Object(id=guild_id) if guild_id else None

    @tree.command(name="about", description="About this bot", guild=guild)
    async def about(interaction: Interaction):
        """Print info about the bot"""
        
        message = """
        This bot was made using a templete from
        https://github.com/CarterPlenge/discord-bot-template
        
        This about command has not been reconfigured from template default. 
        """
        
        await interaction.response.send_message(
            message,
            ephemeral=True
        )