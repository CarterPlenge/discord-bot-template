import importlib
import pkgutil
from ..logger import setup_logger

logger = setup_logger(__name__)

def register_all(tree, database, guild_id):
    """Auto-register all commands inside this category folder."""
    for module in pkgutil.iter_modules(__path__):
        mod = importlib.import_module(f"{__name__}.{module.name}")
        if hasattr(mod, "register"):
            mod.register(tree, database, guild_id)
            logger.info(f"Loaded user command: {module.name}")
