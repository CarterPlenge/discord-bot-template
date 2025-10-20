"""
Commands can be configured from discord server settings.
Not recommended you used this unless you have a specific need. 
"""

from discord import app_commands, Interaction
from functools import wraps

def require_role(role_name: str):
    """restricts a command to a specific role"""
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            if not any(role.name == role_name for role in interaction.user.roles):
                await interaction.response.send_message(
                    f"Must have role: **{role_name}** to use this command.",
                    ephemeral=True
                )
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def require_any_role(*role_names: str):
    """restricts a command to users with any specified role"""
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            user_roles = {role.name for role in interaction.user.roles}
            required_roles = set(role_names)
            if not user_roles & required_roles:
                roles_str = ", ".join(role_names)
                await interaction.response.send_message(
                    f"Must have one of the following roles use this command: {roles_str}",
                    ephemeral=True
                )
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


def require_all_roles(*role_names: str):
    """restricts a command to users with all specified roles"""
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            user_roles = {role.name for role in interaction.user.roles}
            required_roles = set(role_names)
            if not required_roles.issubset(user_roles):
                roles_str = ", ".join(role_names)
                await interaction.response.send_message(
                    f"Must have all of the following roles use this command: {roles_str}",
                    ephemeral=True
                )
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator