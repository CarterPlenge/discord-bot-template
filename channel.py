"""
Commands can be configured from discord server settings.
Not recommended you used this unless you have a specific need. 
"""

from discord import app_commands, Interaction
from functools import wraps

def require_channel(channel_name: str):
    """restricts a command to a specific channel"""
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            if interaction.channel.name != channel_name:
                await interaction.response.send_message(
                    f"This command can only be used in **#{channel_name}**.",
                    ephemeral=True
                )
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator

def require_any_channel(*channel_names: str):
    """restricts a command to any of the specified channels."""
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            if interaction.channel.name not in channel_names:
                channels_str = ", ".join(f"#{ch}" for ch in channel_names)
                await interaction.response.send_message(
                    f"This command can only be used in: {channels_str}",
                    ephemeral=True
                )
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator