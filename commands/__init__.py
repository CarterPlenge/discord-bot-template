import discord
from discord import app_commands
import importlib
import pkgutil
from logger import setup_logger

logger = setup_logger(__name__)

def register_all(tree: app_commands.CommandTree, discord_object: discord.Object):
    """Auto-register all commands inside this category folder."""
    for module in pkgutil.iter_modules(__path__):
        mod = importlib.import_module(f"{__name__}.{module.name}")
        if hasattr(mod, "register"):
            mod.register(tree, discord_object)
            logger.info(f"Loaded user command: {module.name}")
